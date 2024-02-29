from django.shortcuts import render, redirect
from main.models import *
from json import dumps
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import re
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from queue import PriorityQueue
import heapq
from datetime import date, timedelta, datetime
from django.http import JsonResponse
import PyPDF2
import textract
import string
import pandas as pd
import matplotlib.pyplot as plt
import pyotp
import base64
from django.utils import timezone
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from main.utils import send_emails
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json
from django.core.mail import EmailMessage
from jobster import settings
from django.db.models import Subquery
import os
from django.views.decorators.csrf import csrf_exempt
import random
import threading
import json
from scipy.sparse import save_npz, load_npz
from io import BytesIO
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
# Create your views here.


def dashboard(request, pk):
    
    context = Employer.objects.get(eid=pk)
    jobs = Jobs.objects.filter(eid=pk)
    applics = Application.objects.filter(eid=pk)
    visits = ProfileVisits.objects.filter(user_type="e", e_id=pk)
    # jobs = Jobs.objects.all()
    all_notis = []
    count = 0
    recent_candidates = []
    num_notif = Notifications.objects.filter(
        rece_id=context.log_id).order_by('-datetime')
    for i in num_notif:
        single_notis = {}
        single_notis['notif_type'] = i.notif_type
        single_notis['datetime'] = i.datetime
        user = JobSeeker.objects.get(log_id=i.send_id)
        single_notis['name'] = user.name
        single_notis['user_id'] = user.user_id
        single_notis['log_id'] = user.log_id.log_id
        heapq.heappush(recent_candidates, (i.datetime, user.user_id,
                       user.photo, user.name, user.location, user.log_id.log_id))
        # recent_candidates.put([i.datetime, user.user_id, user.photo, user.name, user.title, user.location])
        if i.job_id:
            job = jobs.filter(jobid=i.job_id.jobid)
            single_notis['title'] = job[0].title
            single_notis['jobid'] = job[0].jobid
        if i.testuser_id:
            testinfo = TestInfo.objects.get(test_id=i.testuser_id.test_id)
            single_notis['test_name'] = testinfo.test_name
            single_notis['test_id'] = i.testuser_id.testuser_id
        all_notis.append(single_notis)
        count = count+1
        if (count > 10):
            break
    threads = Threads.objects.filter(sender=context.log_id)
    countunmess = 0
    recent_mess = []
    # for i in applics:
    #     jobseek=JobSeeker.objects.get(user_id=i.user_id.user_id)
    #     heapq.heappush(recent_candidates, (i.date_applied, jobseek.user_id, jobseek.photo, jobseek.name, jobseek.title, jobseek.location))
    for i in threads:
        mess = Messages.objects.filter(
            msg_id=i.msg_id, receiver_user=context.log_id.log_id).order_by("-date")
        if (len(mess) > 0):
            countunmess = countunmess+len(mess.filter(is_read=0))
            tempval = []
            tempval.append(mess[0].date)
            tempval.append(mess[0].body)
            jobseek = JobSeeker.objects.get(log_id=mess[0].sender_user.log_id)
            tempval.append(jobseek.name)
            tempval.append(jobseek.photo)
            heapq.heappush(recent_candidates, (mess[0].date, jobseek.user_id,
                           jobseek.photo, jobseek.name, jobseek.location, jobseek.log_id.log_id))
            # recent_candidates.put([mess[0].date, jobseek.user_id, jobseek.photo, jobseek.name, jobseek.title, jobseek.location])
            recent_mess.append(tempval)
    finalrecent = []
    count = 0
    existing = []
    while recent_candidates:
        temp = recent_candidates.pop()
        if temp[1] not in existing:
            finalrecent.append(temp)
            count = count+1
            if (count > 10):
                break
        existing.append(temp[1])
    recent_mess.sort(reverse=True)
    recent_mess_temp = []
    idx = min(4, len(recent_mess))
    for i in range(0, idx):
        recent_mess_temp.append(recent_mess[i])
    applics_chart = []
    applics_7 = []
    applics_30 = []
    applics_60 = []
    applics_90 = []
    applics_365 = []
    counts = []
    cou = 0

    visits_chart = []
    visits_7 = []
    visits_30 = []
    visits_60 = []
    visits_90 = []
    visits_365 = []
    countsv = []
    couv = 0
    
    # jobs_chart = []
    # jobs_7 = []
    # jobs_30 = []
    # jobs_60 = []
    # jobs_90 = []
    # jobs_365 = []
    # countsj = []
    # couj = 0

    for i in range(0, 365):
        d = date.today()-timedelta(days=i)
        temp = applics.filter(date_applied__year=d.year,
                              date_applied__month=d.month, date_applied__day=d.day)
        n = len(temp)
        heapq.heappush(applics_chart, (-1*(n), n, d))
        cou = cou+n

        temp = visits.filter(visiting_time__year=d.year,
                             visiting_time__month=d.month, visiting_time__day=d.day)
        n = len(temp)
        heapq.heappush(visits_chart, (-1*(n), n, d))
        couv = couv+n

        # temp = jobs.filter(postdate__year=d.year,postdate__month=d.month, postdate__day=d.day)
        # n = len(temp)
        # heapq.heappush(jobs_chart, (-1*(n), n, d))
        # couj = couj+n
        if (len(applics_chart) == 7):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_7.append([applics_chart[j][2], applics_chart[j][1]])
                visits_7.append([visits_chart[j][2], visits_chart[j][1]])
        if (len(applics_chart) == 30):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_30.append([applics_chart[j][2], applics_chart[j][1]])
                visits_30.append([visits_chart[j][2], visits_chart[j][1]])
        if (len(applics_chart) == 60):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_60.append([applics_chart[j][2], applics_chart[j][1]])
                visits_60.append([visits_chart[j][2], visits_chart[j][1]])
        if (len(applics_chart) == 90):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_90.append([applics_chart[j][2], applics_chart[j][1]])
                visits_90.append([visits_chart[j][2], visits_chart[j][1]])
        if (len(applics_chart) == 364):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_365.append([applics_chart[j][2], applics_chart[j][1]])
                visits_365.append([visits_chart[j][2], visits_chart[j][1]])
    
    applics_7.sort()
    applics_30.sort()
    applics_60.sort()
    applics_90.sort()
    applics_365.sort()
    visits_7.sort()
    visits_30.sort()
    visits_60.sort()
    visits_90.sort()
    visits_365.sort()
    
    ############################################################
    
    ############################################################
    charts_context = {}
    charts_context['pastsev'] = dumps([item[1] for item in applics_7])
    charts_context['dates'] = dumps(
        [item[0] for item in applics_7], default=str)
    charts_context['count_7'] = dumps(counts[0])
    charts_context['pastthi'] = dumps([item[1] for item in applics_30])
    charts_context['dates30'] = dumps(
        [item[0] for item in applics_30], default=str)
    charts_context['count_30'] = dumps(counts[1])
    charts_context['pastsix'] = dumps([item[1] for item in applics_60])
    charts_context['dates60'] = dumps(
        [item[0] for item in applics_60], default=str)
    charts_context['count_60'] = dumps(counts[2])
    charts_context['pastnin'] = dumps([item[1] for item in applics_60])
    charts_context['dates90'] = dumps(
        [item[0] for item in applics_60], default=str)
    charts_context['count_90'] = dumps(counts[3])
    charts_context['pastyea'] = dumps([item[1] for item in applics_365])
    charts_context['dates365'] = dumps(
        [item[0] for item in applics_365], default=str)
    charts_context['count_365'] = dumps(counts[4])

    charts_context['vpastsev'] = dumps([item[1] for item in visits_7])
    charts_context['vdates'] = dumps(
        [item[0] for item in visits_7], default=str)
    charts_context['vcount_7'] = dumps(countsv[0])
    charts_context['vpastthi'] = dumps([item[1] for item in visits_30])
    charts_context['vdates30'] = dumps(
        [item[0] for item in visits_30], default=str)
    charts_context['vcount_30'] = dumps(countsv[1])
    charts_context['vpastsix'] = dumps([item[1] for item in visits_60])
    charts_context['vdates60'] = dumps(
        [item[0] for item in visits_60], default=str)
    charts_context['vcount_60'] = dumps(countsv[2])
    charts_context['vpastnin'] = dumps([item[1] for item in visits_90])
    charts_context['vdates90'] = dumps(
        [item[0] for item in visits_90], default=str)
    charts_context['vcount_90'] = dumps(countsv[3])
    charts_context['vpastyea'] = dumps([item[1] for item in visits_365])
    charts_context['vdates365'] = dumps(
        [item[0] for item in visits_365], default=str)
    charts_context['vcount_365'] = dumps(countsv[4])
    nums = [len(jobs), len(applics), countunmess]
    if 'shower' in request.session:
        del request.session['shower']

    feedback_given_jobs = ResumeFeedback.objects.values('job_id')
    jobs_ = Jobs.objects.filter(eid=pk,status=7).exclude(jobid__in=Subquery(feedback_given_jobs))
    
    # print(charts_context)
    return render(request, 'dashboard-employer.html', {'pk': pk, 'nums': nums, 'notifics': all_notis, 'recent': recent_mess_temp, 'candi': finalrecent, 'charts': charts_context, 'counts': counts,'jobs_':jobs_})

def deserialize_sparse_matrix(serialized_data):
    serialized_matrix = serialized_data.encode('latin1')

    buffer = BytesIO(serialized_matrix)
    matrix = load_npz(buffer)
    return matrix

def newjob(request, pk):
    if (request.method == "POST"):
        job = Jobs()
        job.eid = Employer.objects.get(eid=pk)
        job.title = request.POST['title']
        job.location = request.POST['location']
        job.fnarea = request.POST['fnarea']
        job.jobdesc = request.POST['description']
        job.experience = request.POST['experience']
        job.careerlevel = request.POST['careerlevel']
        job.jobtype = request.POST['jobtype']
        job.basicpay = request.POST['basicpay'] +" "+request.POST['basicpaySuffix']
        skills = request.POST.getlist('skills')
        all_skills = ""
        for i in skills:
            all_skills = all_skills+i+","
        #sta = request.POST['reqCand']
        #if(int(sta) == 2):
            #job.status = 6
        # raw_skills = request.POST['skills']
        # normalized_skills = ','.join(skill.strip() for skill in raw_skills.split(','))

        job.skills = all_skills
        # job.responsibilities = request.POST['responsibilities']
        # job.requirements = request.POST['requirements']
        filev = None
        try:
            filev = request.FILES["jobDescriptionFile"]
            lst = filev._name.split(".")
            random_integer = random.randint(1, 10000)
            filev._name = str(pk)+"_"+str(request.POST['title'])+"_job_description"+str(random_integer)+"_"+filev._name
            job.job_desc = filev
        except:
            filev = None
        job.save()
        screening_questions = ScreeningQuestions()
        screening_questions.job_id = job
        screening_questions.questions = request.POST.get('questions', []).join(', ')
        screening_questions.save()


        job_id = job.jobid
        candid = []
        jobid = job_id
        if (jobid):
            try:
                job_ = Jobs.objects.get(jobid=jobid)
                if job_.status == 1 or job_.status == 3:
                    send = True
                job_.status = 5
                job_.save()
                vectorizer = CountVectorizer()
                matching_percentages = []
                important_data_jobs = f"{job_.title} {job_.jobdesc} {job_.fnarea} {job_.skills} {job_.experience} {job_.basicpay} {job_.location} {job_.industry} {job_.ugqual} {job_.pgqual} {job_.profile} {job_.jobtype} {job_.requirements} {job_.responsibilities} {job_.notice_period}"
                job_description = preprocess_text(important_data_jobs)
                total_job_desc_data = f"{job_description}"
                job_description_vector = vectorizer.fit_transform([total_job_desc_data])
                try:
                    job_desc_file = job_.job_desc.path
                    job_text = extract_text_from_pdf(job_desc_file)
                    total_job_desc_data = f"{job_description}{job_text}"
                except:
                    pass
                for job_seeker in JobSeeker.objects.all():
                    try:
                        resume_analysis = ResumeAnalysis.objects.get(jobseeker_id=job_seeker)
                        job_seeker_data_vector = deserialize_sparse_matrix(resume_analysis.sparse_matrix_data)
                        job_seeker_dimensions = job_seeker_data_vector.shape[1]
                        job_description_dimensions = job_description_vector.shape[1]
                        min_dimensions = min(job_seeker_dimensions, job_description_dimensions)
                        job_seeker_data_vector_trimmed = job_seeker_data_vector[:, :min_dimensions]
                        job_description_vector_trimmed = job_description_vector[:, :min_dimensions]
                        cosine_sim_job_seeker = cosine_similarity(job_description_vector_trimmed, job_seeker_data_vector_trimmed)

                        job_matching_percentage = round(cosine_sim_job_seeker[0][0] * 100, 2)
                        job_matcher = JobMatcher(jobseeker=job_seeker, job=job_)
                        match_percentage = job_matcher.calculate_match_percentage()
                        total_matching_percentage = round((job_matching_percentage + match_percentage + 40) / 2, 2)
                        matching_percentages.append((job_seeker.user_id, total_matching_percentage))
                    except Exception as e:
                        pass
                matching_percentages.sort(key=lambda x: x[1], reverse=True)

                top_matching_job_seekers = matching_percentages[:20]
                # print(top_matching_job_seekers)
                if(send):
                    email_thread = threading.Thread(target=send_email_newjob, args=(top_matching_job_seekers,job_.eid.log_id.email))
                    email_thread.start()
                    
                serialized_list = json.dumps(top_matching_job_seekers)
                job_.suggestions = serialized_list
                job_.status = 4
                job_.save()
            except Jobs.DoesNotExist:
                pass
        if (job_):
            
            if job_.status == 4:
                top_matching_job_seekers = job_.suggestions
                python_list = json.loads(top_matching_job_seekers)
                for i in python_list:
                    seek = JobSeeker.objects.get(user_id=i[0])
                    single_candidate = {}
                    single_candidate['user_id'] = seek.user_id
                    single_candidate['name'] = seek.name
                    if seek.photo:
                        single_candidate['photo'] = seek.photo
                    single_candidate['score'] = i[1]
                    single_candidate['location'] = seek.location
                    candid.append(single_candidate)
        request.session['c_s_id'] = job.jobid
        data_ = {'message': 'Success','jobid':job_id}
        if candid:
            data_['candidates'] = dumps(candid, default=str)
        return JsonResponse(data_)
    if 'shower' in request.session:
        del request.session['shower']

    cities = ['Adilabad', 'Agra', 'Ahmedabad', 'Ahmednagar', 'Aizawl', 'Ajitgarh (Mohali)', 'Ajmer', 'Akola', 'Alappuzha', 'Aligarh', 'Alirajpur', 'Allahabad', 'Almora', 'Alwar', 'Ambala', 'Ambedkar Nagar', 'Amravati', 'Amreli district', 'Amritsar', 'Anand', 'Anantapur', 'Anantnag', 'Angul', 'Anjaw', 'Anuppur', 'Araria', 'Ariyalur', 'Arwal', 'Ashok Nagar', 'Auraiya', 'Aurangabad', 'Aurangabad', 'Azamgarh', 'Badgam', 'Bagalkot', 'Bageshwar', 'Bagpat', 'Bahraich', 'Baksa', 'Balaghat', 'Balangir', 'Balasore', 'Ballia', 'Balrampur', 'Banaskantha', 'Banda', 'Bandipora', 'Bangalore Rural', 'Bangalore Urban', 'Banka', 'Bankura', 'Banswara', 'Barabanki', 'Baramulla', 'Baran', 'Bardhaman', 'Bareilly', 'Bargarh (Baragarh)', 'Barmer', 'Barnala', 'Barpeta', 'Barwani', 'Bastar', 'Basti', 'Bathinda', 'Beed', 'Begusarai', 'Belgaum', 'Bellary', 'Betul', 'Bhadrak', 'Bhagalpur', 'Bhandara', 'Bharatpur', 'Bharuch', 'Bhavnagar', 'Bhilwara', 'Bhind', 'Bhiwani', 'Bhojpur', 'Bhopal', 'Bidar', 'Bijapur', 'Bijapur', 'Bijnor', 'Bikaner', 'Bilaspur', 'Bilaspur', 'Birbhum', 'Bishnupur', 'Bokaro', 'Bongaigaon', 'Boudh (Bauda)', 'Budaun', 'Bulandshahr', 'Buldhana', 'Bundi', 'Burhanpur', 'Buxar', 'Cachar', 'Central Delhi', 'Chamarajnagar', 'Chamba', 'Chamoli', 'Champawat', 'Champhai', 'Chandauli', 'Chandel', 'Chandigarh', 'Chandrapur', 'Changlang', 'Chatra', 'Chennai', 'Chhatarpur', 'Chhatrapati Shahuji Maharaj Nagar', 'Chhindwara', 'Chikkaballapur', 'Chikkamagaluru', 'Chirang', 'Chitradurga', 'Chitrakoot', 'Chittoor', 'Chittorgarh', 'Churachandpur', 'Churu', 'Coimbatore', 'Cooch Behar', 'Cuddalore', 'Cuttack', 'Dadra and Nagar Haveli', 'Dahod', 'Dakshin Dinajpur', 'Dakshina Kannada', 'Daman', 'Damoh', 'Dantewada', 'Darbhanga', 'Darjeeling', 'Darrang', 'Datia', 'Dausa', 'Davanagere', 'Debagarh (Deogarh)', 'Dehradun', 'Deoghar', 'Deoria', 'Dewas', 'Dhalai', 'Dhamtari', 'Dhanbad', 'Dhar', 'Dharmapuri', 'Dharwad', 'Dhemaji', 'Dhenkanal', 'Dholpur', 'Dhubri', 'Dhule', 'Dibang Valley', 'Dibrugarh', 'Dima Hasao', 'Dimapur', 'Dindigul', 'Dindori', 'Diu', 'Doda', 'Dumka', 'Dungapur', 'Durg', 'East Champaran', 'East Delhi', 'East Garo Hills', 'East Khasi Hills', 'East Siang', 'East Sikkim', 'East Singhbhum', 'Eluru', 'Ernakulam', 'Erode', 'Etah', 'Etawah', 'Faizabad', 'Faridabad', 'Faridkot', 'Farrukhabad', 'Fatehabad', 'Fatehgarh Sahib', 'Fatehpur', 'Fazilka', 'Firozabad', 'Firozpur', 'Gadag', 'Gadchiroli', 'Gajapati', 'Ganderbal', 'Gandhinagar', 'Ganganagar', 'Ganjam', 'Garhwa', 'Gautam Buddh Nagar', 'Gaya', 'Ghaziabad', 'Ghazipur', 'Giridih', 'Goalpara', 'Godda', 'Golaghat', 'Gonda', 'Gondia', 'Gopalganj', 'Gorakhpur', 'Gulbarga', 'Gumla', 'Guna', 'Guntur', 'Gurdaspur', 'Gurgaon', 'Gwalior', 'Hailakandi', 'Hamirpur', 'Hamirpur', 'Hanumangarh', 'Harda', 'Hardoi', 'Haridwar', 'Hassan', 'Haveri district', 'Hazaribag', 'Hingoli', 'Hissar', 'Hooghly', 'Hoshangabad', 'Hoshiarpur', 'Howrah', 'Hyderabad', 'Hyderabad', 'Idukki', 'Imphal East', 'Imphal West', 'Indore', 'Jabalpur', 'Jagatsinghpur', 'Jaintia Hills', 'Jaipur', 'Jaisalmer', 'Jajpur', 'Jalandhar', 'Jalaun', 'Jalgaon', 'Jalna', 'Jalore', 'Jalpaiguri', 'Jammu', 'Jamnagar', 'Jamtara', 'Jamui', 'Janjgir-Champa', 'Jashpur', 'Jaunpur district', 'Jehanabad', 'Jhabua', 'Jhajjar', 'Jhalawar', 'Jhansi', 'Jharsuguda', 'Jhunjhunu', 'Jind', 'Jodhpur', 'Jorhat', 'Junagadh', 'Jyotiba Phule Nagar', 'Kabirdham (formerly Kawardha)', 'Kadapa', 'Kaimur', 'Kaithal', 'Kakinada', 'Kalahandi', 'Kamrup', 'Kamrup Metropolitan', 'Kanchipuram', 'Kandhamal', 'Kangra', 'Kanker', 'Kannauj', 'Kannur', 'Kanpur', 'Kanshi Ram Nagar', 'Kanyakumari', 'Kapurthala', 'Karaikal', 'Karauli', 'Karbi Anglong', 'Kargil', 'Karimganj', 'Karimnagar', 'Karnal', 'Karur', 'Kasaragod', 'Kathua', 'Katihar', 'Katni', 'Kaushambi', 'Kendrapara', 'Kendujhar (Keonjhar)', 'Khagaria', 'Khammam', 'Khandwa (East Nimar)', 'Khargone (West Nimar)', 'Kheda', 'Khordha', 'Khowai', 'Khunti', 'Kinnaur', 'Kishanganj', 'Kishtwar', 'Kodagu', 'Koderma', 'Kohima', 'Kokrajhar', 'Kolar', 'Kolasib', 'Kolhapur', 'Kolkata', 'Kollam', 'Koppal', 'Koraput', 'Korba', 'Koriya', 'Kota', 'Kottayam', 'Kozhikode', 'Krishna', 'Kulgam', 'Kullu', 'Kupwara', 'Kurnool', 'Kurukshetra', 'Kurung Kumey', 'Kushinagar', 'Kutch', 'Lahaul and Spiti', 'Lakhimpur', 'Lakhimpur Kheri', 'Lakhisarai', 'Lalitpur', 'Latehar', 'Latur', 'Lawngtlai', 'Leh', 'Lohardaga', 'Lohit', 'Lower Dibang Valley', 'Lower Subansiri', 'Lucknow', 'Ludhiana', 'Lunglei', 'Madhepura', 'Madhubani', 'Madurai', 'Mahamaya Nagar', 'Maharajganj', 'Mahasamund', 'Mahbubnagar', 'Mahe', 'Mahendragarh', 'Mahoba', 'Mainpuri', 'Malappuram', 'Maldah', 'Malkangiri', 'Mamit', 'Mandi', 'Mandla', 'Mandsaur', 'Mandya', 'Mansa', 'Marigaon', 'Mathura', 'Mau', 'Mayurbhanj', 'Medak', 'Meerut', 'Mehsana', 'Mewat', 'Mirzapur', 'Moga', 'Mokokchung', 'Mon', 'Moradabad', 'Morena', 'Mumbai City', 'Mumbai suburban', 'Munger', 'Murshidabad', 'Muzaffarnagar', 'Muzaffarpur', 'Mysore', 'Nabarangpur', 'Nadia', 'Nagaon', 'Nagapattinam', 'Nagaur', 'Nagpur', 'Nainital', 'Nalanda', 'Nalbari', 'Nalgonda', 'Namakkal', 'Nanded', 'Nandurbar', 'Narayanpur', 'Narmada', 'Narsinghpur', 'Nashik', 'Navsari', 'Nawada', 'Nawanshahr', 'Nayagarh', 'Neemuch', 'Nellore', 'New Delhi', 'Nilgiris', 'Nizamabad', 'North 24 Parganas', 'North Delhi', 'North East Delhi', 'North Goa', 'North Sikkim', 'North Tripura', 'North West Delhi', 'Nuapada', 'Ongole', 'Osmanabad', 'Pakur', 'Palakkad', 'Palamu', 'Pali', 'Palwal', 'Panchkula', 'Panchmahal', 'Panchsheel Nagar district (Hapur)', 'Panipat', 'Panna', 'Papum Pare', 'Parbhani', 'Paschim Medinipur', 'Patan', 'Pathanamthitta', 'Pathankot', 'Patiala', 'Patna', 'Pauri Garhwal', 'Perambalur', 'Phek', 'Pilibhit', 'Pithoragarh', 'Pondicherry', 'Poonch', 'Porbandar', 'Pratapgarh', 'Pratapgarh', 'Pudukkottai', 'Pulwama', 'Pune', 'Purba Medinipur', 'Puri', 'Purnia', 'Purulia', 'Raebareli', 'Raichur', 'Raigad', 'Raigarh', 'Raipur', 'Raisen', 'Rajauri', 'Rajgarh', 'Rajkot', 'Rajnandgaon', 'Rajsamand', 'Ramabai Nagar (Kanpur Dehat)', 'Ramanagara', 'Ramanathapuram', 'Ramban', 'Ramgarh', 'Rampur', 'Ranchi', 'Ratlam', 'Ratnagiri', 'Rayagada', 'Reasi', 'Rewa', 'Rewari', 'Ri Bhoi', 'Rohtak', 'Rohtas', 'Rudraprayag', 'Rupnagar', 'Sabarkantha', 'Sagar', 'Saharanpur', 'Saharsa', 'Sahibganj', 'Saiha', 'Salem', 'Samastipur', 'Samba', 'Sambalpur', 'Sangli', 'Sangrur', 'Sant Kabir Nagar', 'Sant Ravidas Nagar', 'Saran', 'Satara', 'Satna', 'Sawai Madhopur', 'Sehore', 'Senapati', 'Seoni', 'Seraikela Kharsawan', 'Serchhip', 'Shahdol', 'Shahjahanpur', 'Shajapur', 'Shamli', 'Sheikhpura', 'Sheohar', 'Sheopur', 'Shimla', 'Shimoga', 'Shivpuri', 'Shopian', 'Shravasti', 'Sibsagar', 'Siddharthnagar', 'Sidhi', 'Sikar', 'Simdega', 'Sindhudurg', 'Singrauli', 'Sirmaur', 'Sirohi', 'Sirsa', 'Sitamarhi', 'Sitapur', 'Sivaganga', 'Siwan', 'Solan', 'Solapur', 'Sonbhadra', 'Sonipat', 'Sonitpur', 'South 24 Parganas', 'South Delhi', 'South Garo Hills', 'South Goa', 'South Sikkim', 'South Tripura', 'South West Delhi', 'Sri Muktsar Sahib', 'Srikakulam', 'Srinagar', 'Subarnapur (Sonepur)', 'Sultanpur', 'Sundergarh', 'Supaul', 'Surat', 'Surendranagar', 'Surguja', 'Tamenglong', 'Tarn Taran', 'Tawang', 'Tehri Garhwal', 'Thane', 'Thanjavur', 'The Dangs', 'Theni', 'Thiruvananthapuram', 'Thoothukudi', 'Thoubal', 'Thrissur', 'Tikamgarh', 'Tinsukia', 'Tirap', 'Tiruchirappalli', 'Tirunelveli', 'Tirupur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Tonk', 'Tuensang', 'Tumkur', 'Udaipur', 'Udalguri', 'Udham Singh Nagar', 'Udhampur', 'Udupi', 'Ujjain', 'Ukhrul', 'Umaria', 'Una', 'Unnao', 'Upper Siang', 'Upper Subansiri', 'Uttar Dinajpur', 'Uttara Kannada', 'Uttarkashi', 'Vadodara', 'Vaishali', 'Valsad', 'Varanasi', 'Vellore', 'Vidisha', 'Viluppuram', 'Virudhunagar', 'Visakhapatnam', 'Vizianagaram', 'Vyara', 'Warangal', 'Wardha', 'Washim', 'Wayanad', 'West Champaran', 'West Delhi', 'West Garo Hills', 'West Kameng', 'West Khasi Hills', 'West Siang', 'West Sikkim', 'West Singhbhum', 'West Tripura', 'Wokha', 'Yadgir', 'Yamuna Nagar', 'Yanam', 'Yavatmal', 'Zunheboto'];
    
    roledetails = RoleDetails.objects.all()
    allskills = AllSkills.objects.all()
    return render(request, 'newjob-employer.html', {'pk': pk, 'roledetails': roledetails,'allskills':allskills,'cities':cities})

from django.http import JsonResponse

def get_cand_name(request, pk):
    if request.method == "POST":
        try:
            jobseeker = JobSeeker.objects.get(user_id=request.POST['id'])
            name = jobseeker.name
            return JsonResponse({'name': name}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)
    return JsonResponse({'Error in request method'}, safe=False)



def send_email_newjob(top_matching_job_seekers,emp_mail):
    email_list = []
    for i in top_matching_job_seekers:
        seek = JobSeeker.objects.get(user_id=i[0])
        email_list.append(seek.log_id.email)
    email_subject = "Job Alert"
    message = "You are among top 20 best profiles for this job"
    email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, email_list)
    email.fail_silently = True
    email.send()
    email_subject = "Candidate suggestions"
    message = "Suggestions have been provided for {job_.title} job"
    email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [emp_mail])
    email.fail_silently = True
    email.send()



def matchPerChange(request,pk):
    if request.method == "POST":
        if(request.POST['job_id']):
            job = Jobs.objects.get(jobid = request.POST['job_id'])
            job.match_per = request.POST['job_id']
            job.save()
            return JsonResponse({'message': 'Success'})
        return JsonResponse({'message': 'An error occured'})
    return JsonResponse({'message': 'An error occured'})
  
def edit(request, pk):
    context = Employer.objects.get(eid=pk)
    if request.method == "POST":
        context.ename = request.POST['ename']
        loger = Login.objects.get(email=request.session['email'])
        loger.email = request.POST['email']
        request.session['name'] = request.POST['ename']
        request.session['email'] = request.POST['email']
        # context.phone = request.POST['phone']
        context.website = request.POST['website']
        context.profile = request.POST['profile']
        context.industry = request.POST['industry']
        context.yearfounded = request.POST['yearfounded']
        context.size = request.POST['size']
        context.location = request.POST['location']
        context.city = request.POST['city']
        context.address = request.POST['address']
        context.fblink = request.POST['fblink']
        context.twlink = request.POST['twlink']
        context.inlink = request.POST['inlink']
        context.lnlink = request.POST['lnlink']
        context.email = request.POST['email']
        context.strength = request.POST.get('strength', "")
        context.details = request.POST.get('details', "")
        context.turnover = request.POST.get('turnover', "")
        filev = None
        try:
            filev = request.FILES['logo']
            lst = filev._name.split(".")
            filev._name = str(pk)+"_"+context.ename+"_Photo_"+filev._name
            if context.logo:
                context.logo.delete()
            context.logo = filev
            # if (context.logo):
            #     request.session['photo'] = context.logo.url
        except:
            filev = None
        filev = None
        try:
            filev = request.FILES['cover']
            lst = filev._name.split(".")
            filev._name = str(pk)+"_"+context.ename+"_Cover_"+filev._name
            if context.cover:
                context.cover.delete()
            context.cover = filev
        except:
            filev = None
        context.save()
        emp_ = Employer.objects.get(eid=pk)
        if (emp_.logo):
            request.session['photo'] = context.logo.url
        if (emp_.cover):
            request.session['photo'] = context.cover.url
        return redirect('employer:cedit', pk=pk)
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'profile-employer.html', {'pk': pk, 'context': context})


def returnvalue(phone):
    return str(phone) + str(datetime.date(datetime.now())) + "12345"


def get_ot(request, pk):
    if request.method == "GET":
        key = base64.b32encode(returnvalue(request.GET['phone']).encode())
        OTP = pyotp.TOTP(key, interval=30)
        return JsonResponse({'OTP': OTP.now()})
    return JsonResponse({'OTP': 'X'})


def post_ot(request, pk):
    if (request.method == 'POST'):
        key = base64.b32encode(returnvalue(request.POST['phone'][3:]).encode())
        OTP = pyotp.TOTP(key, interval=30)
        if OTP.verify(int(request.POST['OTP'])):
            return JsonResponse({'message': 'Phone number verified'})
    return JsonResponse({'message': 'Please enter correct OTP'})


def cupd_phone(request, pk):
    if request.method == "POST":
        employ = Employer.objects.get(eid=pk)
        employ.phone = request.POST['phone']
        employ.save()
        return JsonResponse({'message': 'x'})


def manage(request, pk):
    if request.method == "POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                Jobs.objects.filter(jobid=i).delete()
            return redirect('employer:manage', pk=pk)
        Jobs.objects.filter(jobid=request.POST['job_id']).delete()
        return redirect('employer:manage', pk=pk)
    all_jobs = Jobs.objects.filter(eid=pk).order_by('-postdate')
    all_det = []
    for i in all_jobs:
        data = {}
        data['jobid'] = i.jobid
        data['title'] = i.title
        data['location'] = i.location
        data['fnarea'] = i.fnarea
        data['jobtype'] = i.jobtype
        applications = Application.objects.filter(job_id=i.jobid)
        data['num'] = len(applications)
        data['postdate'] = i.postdate
        data['status'] = i.status
        all_det.append(data)
    count = len(all_jobs)
    GET_params = request.GET.copy()
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(all_det, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    if 'shower' in request.session:
        del request.session['shower']
    roledetails = RoleDetails.objects.all()
    return render(request, 'managejob-employer.html', {'pk': pk, 'pe': page_obj, 'count': count,'roledetails':roledetails})

def matchPercent(user,job):
    important_data_jobs = f"{job.title} {job.jobdesc} {job.fnarea} {job.skills} {job.experience} {job.basicpay} {job.location} {job.industry} {job.ugqual} {job.pgqual} {job.profile} {job.jobtype} {job.requirements} {job.responsibilities} {job.notice_period}"
    job_description = preprocess_text(important_data_jobs)
    important_data_jobseeker = f"{user.location} {user.experience} {user.skills} {user.basic_edu} {user.master_edu} {user.other_qual} {user.cursal} {user.expsal} {user.notice_period}"
    job_seeker_data = preprocess_text(important_data_jobseeker)
    resume_pdf_file = user.Resume.path
    resume_text = extract_text_from_pdf(resume_pdf_file)
    resume_text = preprocess_text(resume_text)
    total_job_seeker_data = f"{job_seeker_data}{resume_text}"
    vectorizer = CountVectorizer()
    job_description_vector = vectorizer.fit_transform([job_description])
    job_seeker_data_vector = vectorizer.transform([total_job_seeker_data])
    cosine_sim_job_seeker = cosine_similarity(job_description_vector, job_seeker_data_vector)
    job_matching_percentage = round(cosine_sim_job_seeker[0][0] * 100, 2)
    job_matcher = JobMatcher(jobseeker=user, job=job)
    match_percentage = job_matcher.calculate_match_percentage()
    job_matching_percentage = round((job_matching_percentage+match_percentage)/2,2)
    return job_matching_percentage


def candidates(request, pk):
    shower = ""
    if 'shower' in request.session:
        shower = request.session['shower']
    if request.method == "POST":
        if 'approve' in request.POST:
            apps = Application.objects.get(apply_id=request.POST['apply_id'])
            request.session['shower'] = apps.job_id.jobid
            apps.status = 1
            apps.save()
            notif = Notifications()
            notif.notif_type = "A"
            notif.send_id = apps.eid.log_id
            notif.rece_id = apps.user_id.log_id
            notif.job_id = apps.job_id
            notif.save()
            subject = "Congratulations "+apps.user_id.name+" you are selected!"
            message = "Company: "+apps.job_id.eid.ename+"\nJob: "+apps.job_id.title
            receipt = [apps.user_id.log_id.email]
            send_emails(subject, message, receipt)
            return redirect('employer:candidates', pk=pk)
        if 'reject' in request.POST:
            apps = Application.objects.get(apply_id=request.POST['apply_id'])
            request.session['shower'] = apps.job_id.jobid
            apps.status = 2
            apps.save()
            subject = ""+apps.job_id.title+" Application update"
            message = ""+apps.job_id.eid.ename+"has rejected your application for role of"+apps.job_id.title
            receipt = [apps.user_id.log_id.email]
            send_emails(subject, message, receipt)
            return redirect('employer:candidates', pk=pk)
        if 'act' in request.POST:
            if (request.POST['act'] == "delall"):
                for i in request.POST.getlist('ids[]'):
                    ap = Application.objects.filter(apply_id=i)
                    request.session['shower'] = ap[0].job_id.jobid
                    ap.delete()
            if (request.POST['act'] == "appall"):
                for i in request.POST.getlist('ids[]'):
                    apps = Application.objects.get(apply_id=i)
                    apps.status = 1
                    apps.save()
                    subject = "Congratulations "+apps.user_id.name+" you are selected!"
                    message = "Company: "+apps.job_id.eid.ename+"\nJob: "+apps.job_id.title
                    receipt = [apps.user_id.log_id.email]
                    send_emails(subject, message, receipt)
                    request.session['shower'] = apps.job_id.jobid
            if (request.POST['act'] == "rejall"):
                for i in request.POST.getlist('ids[]'):
                    apps = Application.objects.get(apply_id=i)
                    apps.status = 2
                    apps.save()
                    request.session['shower'] = apps.job_id.jobid
            return redirect('employer:candidates', pk=pk)
        ap = Application.objects.filter(apply_id=request.POST['apply_id'])
        request.session['shower'] = ap[0].job_id.jobid
        ap.delete()
        return redirect('employer:candidates', pk=pk)
    testinfo = TestInfo.objects.filter(eid=pk)
    applics = Application.objects.filter(eid=pk)
    jobs = Jobs.objects.filter(eid=pk).order_by('-postdate')
    app_count = []
    single_apps = []
    for i in jobs:
        app_count.append(len(Application.objects.filter(job_id=i.jobid)))
    if (jobs):
        s_apps = Application.objects.filter(job_id=jobs[0].jobid)
        for i in s_apps:
            single_can = {}
            user = JobSeeker.objects.get(user_id=i.user_id.user_id)
            single_can['user_id'] = user.user_id
            single_can['name'] = user.name
            single_can['location'] = user.location
            single_can['photo'] = user.photo
            job = Jobs.objects.get(jobid=i.job_id.jobid)
            # print("hello1",matchPercent(user,job))
            single_can['match'] = matchPercent(user,job)
            single_can['jobid'] = job.jobid
            single_can['title'] = job.title
            single_can['status'] = i.status
            single_can['date_applied'] = i.date_applied
            single_can['apply_id'] = i.apply_id
            single_can['log_id'] = user.log_id.log_id
            if i.status == 4:
                testinfo1 = TestInfo.objects.get(testinfoid=i.test.testinfoid)
                testuser1 = TestUser.objects.get(
                    test_id=testinfo1.test_id.test_id, user_id=user.user_id,emp_id_id = pk,apply_id = i.apply_id)
                single_can['results'] = (
                    int(testuser1.correct_answers)/int(testuser1.total_ques))*100
                single_can['test_id'] = testuser1.testuser_id
            elif i.status == 9:
                candidatetemplate=CandidateTemplateAssignments.objects.get(application_id=i.apply_id)
                single_can['templatesteps']=candidatetemplate.current_step_order-1
                single_can['totalsteps']=len(TemplateSteps.objects.filter(template_id=candidatetemplate.template_id.template_id))
            else:
                single_can['results'] = 0
            single_apps.append(single_can)
    all_can = []
    for i in applics:
        single_can = {}
        user = JobSeeker.objects.get(user_id=i.user_id.user_id)
        job = Jobs.objects.get(jobid=i.job_id.jobid)
        # print("hello2",matchPercent(user,job))
        single_can['user_id'] = user.user_id
        single_can['name'] = user.name
        single_can['location'] = user.location
        single_can['photo'] = user.photo
        single_can['jobid'] = job.jobid
        single_can['title'] = job.title
        single_can['status'] = i.status
        single_can['date_applied'] = i.date_applied
        single_can['apply_id'] = i.apply_id
        single_can['log_id'] = user.log_id.log_id
        single_can['match'] = matchPercent(user,job)
        if i.status == 4:
            testinfo1 = TestInfo.objects.get(testinfoid=i.test.testinfoid)
            testuser1 = TestUser.objects.get(
                test_id=testinfo1.test_id.test_id, user_id=user.user_id,emp_id_id = pk,apply_id = i.apply_id)
            single_can['test_id'] = testuser1.testuser_id
            single_can['results'] = (
                int(testuser1.correct_answers)/int(testuser1.total_ques))*100
        else:
            single_can['results'] = 0
        all_can.append(single_can)
    count = len(all_can)
    all_can = sorted(all_can, key=lambda d: d['date_applied'])
    all_can.reverse()
    GET_params = request.GET.copy()
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(all_can, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    jobs_ = Jobs.objects.filter(eid=pk).exclude(status=4)  
    templates=Templates.objects.filter(emp_id=pk)
    return render(request, 'candidate-employer.html', {'pk': pk, 'pe': page_obj, 'count': count, 'jobs': jobs, 'app_count': app_count, 'single': single_apps, 'shower': shower, 'test': testinfo,'jobs_':jobs_, 'templates': templates})


def interview_complete(request,pk):
    inter = Interview.objects.get(apply_id = request.POST['apply_id'])
    applics = Application.objects.get(apply_id = request.POST['apply_id'])
    applics.status = 6
    applics.save()
    inter.is_done = 1
    inter.save()
    return JsonResponse({'info': "interview Marked Completed"})



def get_candidate(request, pk):
    candidate = JobSeeker.objects.get(user_id=request.GET['user_id'])
    loger = Login.objects.get(log_id=candidate.log_id.log_id)
    cand = {}
    emp = Employer.objects.get(eid=pk)
    if (candidate.photo):
        cand['photo'] = candidate.photo.url
    cand['name'] = candidate.name
    cand['email'] = loger.email
    cand['location'] = candidate.location
    cand['phone'] = candidate.phone
    if (candidate.skills):
        cand['skills'] = candidate.skills.split(",")
    cand['resumeLink'] = candidate.Resume.url
    work = ExperienceJob.objects.filter(user_id=candidate.user_id)
    edu = Education.objects.filter(user_id=candidate.user_id)
    visit = ProfileVisits()
    visit.e_id = emp
    visit.user_id = candidate
    visit.user_type = "c"
    visit.save()
    notif = Notifications()
    notif.notif_type = "V"
    notif.send_id = Login.objects.get(email=request.session['email'])
    notif.rece_id = loger
    notif.save()
    return JsonResponse({'info': dumps(cand, default=str), 'work': dumps(list(work.values())), 'edu': dumps(list(edu.values()))})


def subscriptions(request, pk):
    return render(request, 'subscriptions-employer.html', {'pk': pk})


def change_pass(request, pk):
    if request.method == "POST":
        user = Login.objects.get(email=request.session['email'])
        if (check_password(request.POST['old'], user.password)):
            if request.POST['new'] != request.POST['cnew']:
                messages.error(
                    request, "Both your password and your confirmation password must be exactly same")
                return redirect('employer:cedit', pk=pk)
            if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['new']):
                messages.error(request, "Please entere a valid password")
                return redirect('employer:cedit', pk=pk)
            if (request.POST['old'] == request.POST['new']):
                messages.error(request, "Old and new password cant be same")
                return redirect('employer:cedit', pk=pk)
            user.password = make_password(request.POST['new'])
            user.save()
            request.session['password'] = user.password
            messages.success(request, 'Password changed successfully')
            return redirect('employer:cedit', pk=pk)
        else:
            messages.error(request, "Please enter correct old password")
            return redirect('employer:cedit', pk=pk)
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'password-employer.html', {'pk': pk})


def cinbox(request, pk):
    shower = ""
    if 'thread' in request.session:
        shower = request.session['thread']
        del request.session['thread']
    loger = Login.objects.get(email=request.session['email'])
    threads = Threads.objects.filter(sender=loger.log_id)
    temp_threads = [dumps(list(threads.values()), default=str)]
    all_threads = []
    all_messages = []
    messages = []
    for i in threads:
        single_thread = {}
        mess = Messages.objects.filter(msg_id=i.msg_id).order_by("date")
        messages.append(dumps(list(mess.values()), default=str))
        all_messages.append(mess)
        n = len(mess)
        if (n == 0):
            single_thread['date'] = i.date
            single_thread['body'] = ""
            single_thread['end'] = "x"
        else:
            single_thread['date'] = mess[n-1].date
            single_thread['body'] = mess[n-1].body
            if (mess[n-1].sender_user.log_id == loger.log_id):
                single_thread['end'] = "y"
            else:
                single_thread['end'] = "c"
        single_thread['msg_id'] = i.msg_id
        recei = JobSeeker.objects.get(log_id=i.receiver.log_id)
        single_thread['name'] = recei.name
        single_thread['photo'] = recei.photo
        single_thread['sender'] = i.sender
        single_thread['receiver'] = i.receiver
        all_threads.append(single_thread)
    all_threads.reverse()
    all_messages.reverse()
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'cinbox-employer.html', {'pk': pk, 'threads': all_threads, 'm': all_messages, 'mess': messages, 'thre': temp_threads, 'shower': shower})


def sendmess(request, pk):
    if (request.method == "POST"):
        thread = Threads.objects.get(msg_id=request.POST['candidate'])
        message = Messages()
        message.msg_id = thread
        message.sender_user = Login.objects.get(email=request.session['email'])
        message.receiver_user = Login.objects.get(
            log_id=thread.receiver.log_id)
        message.body = request.POST['message']
        message.save()
        user = Login.objects.get(email=request.session['email'])
        threads = Threads.objects.filter(sender=user.log_id)
        temp_threads = [dumps(list(threads.values()), default=str)]
        messages = []
        temp_messages = []
        for i in threads:
            mess = Messages.objects.filter(msg_id=i.msg_id)
            messages.append(dumps(list(mess.values()), default=str))
            temp_messages.append(mess)
        notif = Notifications()
        notif.notif_type = "M"
        notif.send_id = Login.objects.get(email=request.session['email'])
        notif.rece_id = Login.objects.get(log_id=thread.receiver.log_id)
        notif.save()
        return JsonResponse({'message': 'Y', 'id': request.POST['candidate'], 'thre': temp_threads, 'm': messages})


def fetch(request, pk):
    if request.GET['candidate'] == "":
        return JsonResponse({'message': 'X'})
    user = Login.objects.get(email=request.session['email'])
    threads = Threads.objects.filter(sender=user.log_id)
    temp_threads = [dumps(list(threads.values()), default=str)]
    messages = []
    temp_messages = []
    mess_all = []
    urlval = ""
    count = 0
    ind_unread = []
    rece = []
    for i in threads:
        mess = Messages.objects.filter(
            msg_id=i.msg_id, receiver_user=user.log_id, is_read=False)
        si = len(mess)
        count = si+count
        ind_unread.append([i.msg_id, si])
        messages.append(dumps(list(mess.values()), default=str))
        temp_messages.append(mess)
        mess = Messages.objects.filter(msg_id=i.msg_id)
        n = len(mess)
        if (n > 0):
            if (mess[n-1].sender_user.log_id == user.log_id):
                rece.append({'msg_id': i.msg_id, 'body': "You: " +
                            mess[len(mess)-1].body, 'type': "e"})
            else:
                username = JobSeeker.objects.get(
                    log_id=mess[n-1].sender_user.log_id)
                rece.append({'msg_id': i.msg_id, 'body': username.name +
                            ": "+mess[len(mess)-1].body, 'type': "c"})
        mess_all.append(dumps(list(mess.values()), default=str))
    comp_thread = Threads.objects.get(msg_id=request.GET['candidate'])
    comp_log = Login.objects.get(log_id=comp_thread.receiver.log_id)
    thread = dumps(list(Threads.objects.filter(
        msg_id=request.GET['candidate']).values()), default=str)
    messa = dumps(list(Messages.objects.filter(
        msg_id=request.GET['candidate'], receiver_user=user.log_id, is_read=False).values()), default=str)
    company = dumps(list(JobSeeker.objects.filter(
        log_id=comp_log).values()), default=str)
    try:
        urlval = JobSeeker.objects.filter(log_id=comp_log)[0].photo.url
    except:
        urlval = None
    return JsonResponse({'message': 'Y', 'url': "", 'mess': messages, 'thre': temp_threads, 'count': count, 'thread': thread, 'company': company, 'messa': messa, 'all_mess': mess_all, 'image': urlval, 'unread': dumps(ind_unread), 'rece': dumps(rece)})


def seen(request, pk):
    loger = Login.objects.get(email=request.session['email'])
    if (request.method == "POST"):
        if request.POST['candidate'] == "":
            return JsonResponse({'message': 'X'})
        messages = Messages.objects.filter(
            msg_id=request.POST['candidate'], receiver_user=loger.log_id, is_read=False)
        Messages.objects.filter(
            msg_id=request.POST['candidate'], receiver_user=loger.log_id, is_read=False).update(is_read=True)
        for i in messages:
            i.is_read = True
            i.save()
        return JsonResponse({'message': 'Y'})


def inbox_count(request, pk):
    # user=JobSeeker.objects.get(user_id=pk)
    # num_mess=Threads.objects.filter(receiver=user.log_id, has_unread=1)
    loger = Login.objects.get(email=request.session['email'])
    countval = len(Messages.objects.filter(
        receiver_user=loger.log_id, is_read=False))
    return JsonResponse({'count': countval})


def delete_mess(request, pk):
    if request.method == "POST":
        Threads.objects.get(msg_id=request.POST['candidate']).delete()
        return JsonResponse({'message': 'a'})


def createthread(request, pk):
    if request.method == "POST":
        loger = Employer.objects.get(eid=pk)
        msg = Threads.objects.filter(
            sender=loger.log_id.log_id, receiver=request.POST['receiver'])
        if (len(msg) > 0):
            request.session['thread'] = msg[0].msg_id
            return JsonResponse({'url': ""})
        else:
            newthread = Threads()
            newthread.sender = loger.log_id
            newthread.receiver = Login.objects.get(
                log_id=request.POST['receiver'])
            newthread.save()
            request.session['thread'] = newthread.msg_id
            return JsonResponse({'url': ""})
    return JsonResponse({'url': ""})


def cnotifications(request, pk):
    loger = Login.objects.get(email=request.session['email'])
    # for key, value in request.session.items():
    #     print(f"Key: {key}, Value: {value}")
    notifs = Notifications.objects.filter(
        rece_id=loger.log_id).order_by('-datetime')
    nots = []
    for i in notifs:
        i.readed = True
        i.save()
        request.session['notifnum'] = 0
        single_notif = {}
        single_notif['notif_id'] = i.notif_id
        single_notif['notif_type'] = i.notif_type
        single_notif['datetime'] = i.datetime
        user = JobSeeker.objects.get(log_id=i.send_id)
        single_notif['user_id'] = user.user_id
        single_notif['log_id'] = user.log_id
        single_notif['name'] = user.name
        if i.job_id:
            jobs = Jobs.objects.get(jobid=i.job_id.jobid)
            single_notif['title'] = jobs.title
            single_notif['jobid'] = jobs.jobid
        if i.testuser_id:
            testinfo = TestInfo.objects.get(test_id=i.testuser_id.test_id)
            single_notif['test_name'] = testinfo.test_name
            single_notif['test_id'] = i.testuser_id.testuser_id
        nots.append(single_notif)
    GET_params = request.GET.copy()
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(nots, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'cnotifications-employer.html', {'pk': pk, 'notif': page_obj})





def jobapp(request, pk):
    jobinfo = Jobs.objects.filter(jobid=request.GET['jobid'])
    employer = Employer.objects.filter(eid=pk)
    image = ""
    if (employer[0].logo):
        image = str(employer[0].logo.url)
    return JsonResponse({'logo': image, 'info': dumps(list(jobinfo.values()), default=str), 'company': dumps(list(employer.values()))})


def edit_job(request, pk):
    job = None
    if (request.method == "GET"):
        job = Jobs.objects.filter(jobid=request.GET['jobid'])
    else:
        job = Jobs.objects.filter(jobid=request.POST['jobid'])
    if request.method == "POST":
        if (len(job) > 0):
            job[0].title = request.POST['title']
            job[0].location = request.POST['location']
            job[0].fnarea = request.POST['fnarea']
            job[0].jobdesc = request.POST['description']
            job[0].experience = request.POST['experience']
            job[0].careerlevel = request.POST['careerlevel']
            job[0].jobtype = request.POST['jobtype']
            job[0].basicpay = request.POST['basicpay'] +" "+request.POST['basicpaySuffix']
            job[0].skills = request.POST['skills']
            job[0].responsibilities = request.POST['responsibilities']
            job[0].requirements = request.POST['requirements']
            try:
                if 'jobDescriptionFile' in request.FILES:
                    filev = request.FILES['jobDescriptionFile']
                    # print("hi",filev)
                    lst = filev._name.split(".")
                    random_integer = random.randint(1, 10000)
                    filev._name = str(pk)+"_"+str(request.POST['title'])+"_job_description"+str(random_integer)+"_"+filev._name
                    if job[0].job_desc:
                        job[0].job_desc.delete()
                    job[0].job_desc = filev
            except:
                filev = None 
            job[0].save()
        return redirect('employer:manage', pk=pk)
    return JsonResponse({'info': dumps(list(job.values()), default=str)})

class JobMatcher:
    def __init__(self, jobseeker, job):
        self.jobseeker = jobseeker
        self.job = job
    
    

    def calculate_match_percentage(self):
        total_params = 5  
        matched_params = 0

        if self.jobseeker.skills and self.job.skills:
            job_skills = set(self.job.skills.lower().split(','))
            seeker_skills = set(self.jobseeker.skills.lower().split(','))
            if job_skills.intersection(seeker_skills):
                matched_params += 1

        # Check if location matches
        if self.job.location and self.jobseeker.location:
            if self.job.location.lower() == self.jobseeker.location.lower():
                matched_params += 1

        # Check if notice period matches
        if self.job.notice_period and self.jobseeker.notice_period:
            if self.job.notice_period.lower() == self.jobseeker.notice_period.lower():
                matched_params += 1

        # Check if Experience matches
        if self.jobseeker.experience and self.job.experience:
            if int(self.jobseeker.experience) >= int(self.job.experience):
                matched_params += 1

        # Check if expected salary matches
        # if self.jobseeker.expsal and self.job.basicpay:
        #     if self.jobseeker.expsal <= int(self.job.basicpay):
        #         matched_params += 1

        # Calculate match percentage
        match_percentage = (matched_params / total_params) * 100

        return match_percentage

    def get_matching_details(self):
        matching_details = {}

        # Check if skills match
        if self.jobseeker.skills and self.job.skills:
            job_skills = set(self.job.skills.lower().split(','))
            seeker_skills = set(self.jobseeker.skills.lower().split(','))
            matching_details['skills'] = {
                'match': list(job_skills.intersection(seeker_skills)),
                'not_match': list(job_skills.difference(seeker_skills))
            }
            

        # Check if location matches
        if self.job.location and self.jobseeker.location:
            matching_details['location'] = {
                'match': True if self.job.location.lower() == self.jobseeker.location.lower() else False
            }

        # Check if notice period matches
        if self.job.notice_period and self.jobseeker.notice_period:
            matching_details['notice_period'] = {
                'match': True if self.job.notice_period.lower() == self.jobseeker.notice_period.lower() else False
            }

        # Check if current salary matches
        if self.jobseeker.cursal and self.job.basicpay:
            matching_details['experience'] = {
                'match': True if int(self.jobseeker.experience) >= int(self.job.experience) else False
            }

        # Check if expected salary matches
        # if self.jobseeker.expsal and self.job.basicpay:
        #     matching_details['expected_salary'] = {
        #         'match': True if self.jobseeker.expsal <= int(self.job.basicpay) else False
        #     }

        return matching_details

def preprocess_text(text):
    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]

    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    preprocessed_text = ' '.join(words)
    return preprocessed_text



def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text
def cand_suggest(request, pk):
    job = Jobs.objects.filter(eid=pk).exclude(suggestions="[]")
    candid = []
    sel = ""
    # if ('job_id' in request.GET and request.GET['job_id'] != 'a') or 'c_s_id' in request.session:
    #     print('hello')
    #     single_job = None
    #     if 'c_s_id' in request.session:
    #         sel = int(request.session['c_s_id'])
    #         single_job = Jobs.objects.get(jobid=request.session['c_s_id'])
    #         del request.session['c_s_id']
    #     else:
    #         sel = int(request.GET['job_id'])
    #         single_job = Jobs.objects.get(jobid=request.GET['job_id'])
    #     jobs = JobSeeker.objects.all()
    #     for i in jobs:
    #         if i.Resume:

    #             try:
    #                 pdfFileObj = open("media/"+str(i.Resume), 'rb')
    #                 pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #             except:
    #                 continue
    #             num_pages = pdfReader.numPages
    #             count = 0
    #             text = ""
    #             while count < num_pages:
    #                 pageObj = pdfReader.getPage(count)
    #                 count += 1
    #                 text += pageObj.extractText()
    #             text = text.lower()
    #             text = re.sub(r'\d+', '', text)
    #             text = text.translate(
    #                 str.maketrans('', '', string.punctuation))
    #             terms = {'Python Developer': ['black belt', 'capability analysis', 'control charts', 'doe', 'dmaic', 'fishbone',
    #                                           'gage r&r', 'green belt', 'ishikawa', 'iso', 'kaizen', 'kpi', 'lean', 'metrics',
    #                                           'pdsa', 'performance improvement', 'process improvement', 'quality',
    #                                           'quality circles', 'quality tools', 'root cause', 'six sigma',
    #                                           'stability analysis', 'statistical analysis', 'tqm'],
    #                      'Django Developer': ['automation', 'bottleneck', 'constraints', 'cycle time', 'efficiency', 'fmea',
    #                                           'machinery', 'maintenance', 'manufacture', 'line balancing', 'oee', 'operations',
    #                                           'operations research', 'optimization', 'overall equipment effectiveness',
    #                                           'pfmea', 'process', 'process mapping', 'production', 'resources', 'safety',
    #                                           'stoppage', 'value stream mapping', 'utilization'],
    #                      'React Developer': ['abc analysis', 'apics', 'customer', 'customs', 'delivery', 'distribution', 'eoq', 'epq',
    #                                          'fleet', 'forecast', 'inventory', 'logistic', 'materials', 'outsourcing', 'procurement',
    #                                          'reorder point', 'rout', 'safety stock', 'scheduling', 'shipping', 'stock', 'suppliers',
    #                                          'third party logistics', 'transport', 'transportation', 'traffic', 'supply chain',
    #                                          'vendor', 'warehouse', 'wip', 'work in progress'],
    #                      'NEXT Developer': ['administration', 'agile', 'budget', 'cost', 'direction', 'feasibility analysis',
    #                                         'finance', 'kanban', 'leader', 'leadership', 'management', 'milestones', 'planning',
    #                                         'pmi', 'pmp', 'problem', 'project', 'risk', 'schedule', 'scrum', 'stakeholders'],
    #                      'Project management': ['administration', 'agile', 'budget', 'cost', 'direction', 'feasibility analysis',
    #                                             'finance', 'kanban', 'leader', 'leadership', 'management', 'milestones', 'planning',
    #                                             'pmi', 'pmp', 'problem', 'project', 'risk', 'schedule', 'scrum', 'stakeholders'],
    #                      'Data analytics': ['analytics', 'api', 'aws', 'big data', 'busines intelligence', 'clustering', 'code',
    #                                         'coding', 'data', 'database', 'data mining', 'data science', 'deep learning', 'hadoop',
    #                                         'hypothesis test', 'iot', 'internet', 'machine learning', 'modeling', 'nosql', 'nlp',
    #                                         'predictive', 'programming', 'python', 'r', 'sql', 'tableau', 'text mining',
    #                                         'visualuzation'], }
    #             quality = 0
    #             for area in terms.keys():
    #                 if area.lower() == single_job.title.lower():
    #                     for word in terms[area]:
    #                         if word in text:
    #                             quality += 1
    #                     break
    #             single_candidate = {}
    #             single_candidate['user_id'] = i.user_id
    #             single_candidate['name'] = i.name
    #             if i.photo:
    #                 single_candidate['photo'] = i.photo
    #             single_candidate['score'] = quality
    #             single_candidate['location'] = i.location
    #             candid.append(single_candidate)
    GET_params = request.GET.copy()
    # print("hello1",request.GET['job_id'])
    #############################################################################
    if ('job_id' in request.GET):
        job_ = Jobs.objects.get(jobid=request.GET['job_id'])
        sel = int(request.GET['job_id'])
        if job_.status == 4:
            top_matching_job_seekers = job_.suggestions
            python_list = json.loads(top_matching_job_seekers)
            # print(python_list)
            for i in python_list:
                seek = JobSeeker.objects.get(user_id=i[0])
                single_candidate = {}
                single_candidate['user_id'] = seek.user_id
                single_candidate['name'] = seek.name
                if seek.photo:
                    single_candidate['photo'] = seek.photo
                single_candidate['score'] = i[1]
                single_candidate['location'] = seek.location
                candid.append(single_candidate)

    #############################################################################
    count = len(candid)
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(candid, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    if 'shower' in request.session:
        del request.session['shower']
    # print(sel)
    return render(request, 'suggestions-employer.html', {'pk': pk, 'jobs': job, 'count': count, 'pe': page_obj, 'sel': sel})


def get_cands(request, pk):
    applics = Application.objects.filter(job_id=request.GET['jobid'])
    single_apps = []
    for i in applics:
        single_can = {}
        user = JobSeeker.objects.get(user_id=i.user_id.user_id)
        job = Jobs.objects.get(jobid=i.job_id.jobid)
        single_can['match'] = matchPercent(user,job)
        single_can['user_id'] = user.user_id
        single_can['name'] = user.name
        single_can['location'] = user.location
        try:
            single_can['photo'] = user.photo.url
        except:
            single_can['photo'] = None
        single_can['jobid'] = job.jobid
        single_can['title'] = job.title
        single_can['status'] = i.status
        if i.status == 4:
            testinfo1 = TestInfo.objects.get(testinfoid=i.test.testinfoid)
            testuser1 = TestUser.objects.get(
                test_id=testinfo1.test_id.test_id, user_id=user.user_id,emp_id=pk,apply_id = i.apply_id)
            single_can['results'] = (
                int(testuser1.correct_answers)/int(testuser1.total_ques))*100
            single_can['test_id'] = testuser1.testuser_id
        elif i.status == 9:
            candidatetemplate=CandidateTemplateAssignments.objects.get(application_id=i.apply_id)
            single_can['templatesteps']=candidatetemplate.current_step_order-1
            single_can['totalsteps']=len(TemplateSteps.objects.filter(template_id=candidatetemplate.template_id.template_id))
        else:
            single_can['results'] = 0
        single_can['date_applied'] = i.date_applied
        single_can['apply_id'] = i.apply_id
        single_can['log_id'] = user.log_id.log_id
        single_apps.append(single_can)
    return JsonResponse({'info': dumps(single_apps, default=str)})


def quiz(request, pk):
    quizzes = Quiz.objects.filter(eid=pk)
    quiz = []
    for i in quizzes:
        single_quiz = {}
        single_quiz['quiz_id'] = i.quiz_id
        single_quiz['created_date'] = i.created_date
        single_quiz['time_limit'] = i.time_limit
        job = Jobs.objects.get(jobid=i.job_id.jobid)
        single_quiz['jobid'] = job.jobid
        single_quiz['location'] = job.location
        single_quiz['title'] = job.title
        single_quiz['fnarea'] = job.fnarea
        single_quiz['jobtype'] = job.jobtype
        quiz.append(single_quiz)
    GET_params = request.GET.copy()
    count = len(quizzes)
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(quiz, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'quiz-employer.html', {'pk': pk, 'count': count, 'pe': page_obj})


def show_tests(request, pk):
    if request.method == "POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                Test.objects.get(test_id=i).delete()
            return redirect('employer:show_tests', pk=pk)
        Test.objects.get(test_id=request.POST['test_id']).delete()
        return redirect('employer:show_tests', pk=pk)
    tests = TestInfo.objects.filter(eid=pk)
    all_tests = []
    for i in tests:
        single_test = {}
        single_test['test_id'] = i.test_id.test_id
        single_test['testinfoid'] = i.testinfoid
        single_test['created_date'] = i.test_id.created_date
        single_test['time_limit'] = i.time_limit
        single_test['name'] = i.test_name
        questions = TestQues.objects.filter(testinfoid=i.testinfoid)
        single_test['num'] = len(questions)
        all_tests.append(single_test)
    sorted(all_tests, key=lambda i: i['created_date'])
    all_tests.reverse()
    GET_params = request.GET.copy()
    count = len(all_tests)
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(all_tests, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'show-employer.html', {'pk': pk, 'pe': page_obj, 'count': count})
@csrf_exempt
def edit_test(request,pk):
    if request.method == "POST":
        
        try:
            testinfoid = request.POST.get('testinfoid')
            data = json.loads(request.POST.get('questions'))  # Parse the JSON data
            single_ = TestInfo.objects.get(test_id=testinfoid)
            single_.test_name = request.POST.get('test_name')
            single_.time_limit = request.POST.get('time_limit')
            # print(single_.test_name,single_.time_limit,request.POST.get('test_name'),request.POST.get('time_limit'))
            for i, question_data in enumerate(data):
                single = TestQues.objects.get(ques_id=question_data['ques_id'])
                single.ques_name = question_data['question']
                single.option1 = question_data['options'][0]
                single.option2 = question_data['options'][1]
                single.option3 = question_data['options'][2]
                single.option4 = "Hello"
                single.correct = question_data['correctAnswer']
                single.save()
            single_.save()
        except Exception as e:
            JsonResponse({'message': 'Error updating Test'})
        return JsonResponse({'message': 'Edited'})

def create_test(request, pk):
    if request.method == "POST":
        test = Test()
        test.save()
        testinfo = TestInfo()
        testinfo.test_id = test
        testinfo.test_name = request.POST['name']
        testinfo.eid = Employer.objects.get(eid=pk)
        testinfo.time_limit = request.POST['timelimit']
        testinfo.save()
        info = request.POST.getlist('desc')
        options = request.POST.getlist('optdesc')
        correct = request.POST.getlist('correct')
        n = len(info)
        count = 0
        for i in range(0, n):
            single = TestQues()
            single.testinfoid = testinfo
            single.ques_name = info[i]
            single.option1 = options[count]
            single.option2 = options[count+1]
            single.option3 = options[count+2]
            single.option4 = options[count+3]
            filev = None
            try:
                filev = request.FILES[f"image_{i+1}"]
                lst = filev._name.split(".")
                random_integer = random.randint(1, 10000)
                filev._name = str(testinfo.testinfoid)+"_test_image"+str(random_integer)+"_"+filev._name
                single.images = filev
            except:
                filev = None
            count = count+4
            single.correct = correct[i]
            single.save()
        if request.GET.get('redirect'):
            return redirect('employer:candidates', pk=pk)
        else:
            return redirect('employer:show_tests', pk=pk)

    return render(request, 'create_quiz-employer.html', {'pk': pk})


def schedule(request, pk):
    if request.method == "POST":
        date_time_str = request.POST['date_time']
        desired_datetime = timezone.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M")
        aware_datetime = timezone.make_aware(desired_datetime)
        ist_datetime = aware_datetime + timezone.timedelta(hours=5, minutes=30)
        # + timezone.timedelta(hours=5, minutes=30)
        if 'ids[]' in request.POST:
            ids = request.POST.getlist('ids[]')
            f = False
            for i in ids:
                flag = False
                applics = Application.objects.get(apply_id=i)
                if applics.status == 3:
                    flag = True
                    f = True
                if (flag == False):
                    testinfo = TestInfo.objects.get(
                        testinfoid=request.POST['testinfoid'])
                    tuser = TestUser.objects.filter(
                        user_id=applics.user_id, test_id=testinfo.test_id.test_id)
                    if (len(tuser) > 0):
                        break
                    applics.status = 3
                    request.session['shower'] = applics.job_id.jobid
                    testuser = TestUser()
                    # print("hellooooooo",applics.eid)
                    testuser.emp_id = applics.eid
                    testuser.apply_id = applics
                    testuser.date = ist_datetime
                    testuser.user_id = applics.user_id
                    testuser.test_id = testinfo.test_id
                    applics.test = testinfo
                    applics.save()
                    testuser.save()
                    notif = Notifications()
                    notif.notif_type = "T"
                    notif.send_id = Login.objects.get(
                        email=request.session['email'])
                    notif.rece_id = applics.user_id.log_id
                    notif.save()
                    subject = "Test scheduled by "+applics.job_id.eid.ename
                    message = "Test Name: "+testinfo.test_name + \
                        "\nDuration: "+str(testinfo.time_limit)
                    receipt = [applics.user_id.log_id.email]
                    send_emails(subject, message, receipt)
            return JsonResponse({'message': 'scheduled'})
        applics = Application.objects.get(apply_id=request.POST['id'])
        if applics.status == 3:
            # print("status")

            return JsonResponse({'message': 'X'})
        # print("hello")
        testinfo = TestInfo.objects.get(testinfoid=request.POST['testinfoid'])
        # print(applics.user_id,testinfo.test_id.test_id)
        tuser = TestUser.objects.filter(
            user_id=applics.user_id, test_id=testinfo.test_id.test_id)
        # con_user = TestUser.objects.filter(user_id=applics.user_id, test_id=testinfo.test_id.test_id,jobid = applics.job_id.jobid)
        # if (len(con_user) > 0):
        #     print("testuser")
        #     return JsonResponse({'message': 'X'})
        
        applics.status = 3
        request.session['shower'] = applics.job_id.jobid
        testuser = TestUser()
        testuser.user_id = applics.user_id
        testuser.test_id = testinfo.test_id
        # print("hello",applics.eid.eid)
        testuser.emp_id = applics.eid
        testuser.apply_id = applics
        testuser.date = ist_datetime
        applics.test = testinfo
        applics.save()
        testuser.save()
        notif = Notifications()
        notif.notif_type = "T"
        notif.send_id = Login.objects.get(email=request.session['email'])
        notif.rece_id = applics.user_id.log_id
        notif.save()
        subject = "Test scheduled by "+applics.job_id.eid.ename
        message = "Test Name: "+testinfo.test_name + \
            "\nDuration: "+str(testinfo.time_limit)
        receipt = [applics.user_id.log_id.email]
        send_emails(subject, message, receipt)
    return JsonResponse({'message': 'scheduled'})


def test_info(request, pk):
    testinfo = TestInfo.objects.filter(testinfoid=request.GET['testinfoid'])
    testdate = str(testinfo[0].test_id.created_date)
    testquest = TestQues.objects.filter(testinfoid=testinfo[0].testinfoid)
    testdate = testdate[0:11]
    return JsonResponse({'message': 'x', 'test': dumps(list(testinfo.values()), default=str), 'date': dumps(testdate, default=str), 'ques': dumps(list(testquest.values()))})


def get_results(request, pk):
    testuser = TestUser.objects.get(testuser_id=request.GET['id'],emp_id=pk)
    testinfo = TestInfo.objects.get(test_id=testuser.test_id.test_id)
    data = {}
    data['user_id'] = testuser.user_id.user_id
    # inters = Interview.objects.filter(user_id=testuser.user_id.user_id, eid_id=pk,apply_id = request.GET['applyid'])
    # print(inters)
    data['user_name'] = testuser.user_id.name
    data['name'] = testinfo.test_name
    data['num'] = testuser.total_ques
    data['correct'] = testuser.correct_answers
    data['date'] = testuser.date
    # if (len(inters) > 0):
        # data['int_link'] = inters[0].int_link
    # else:
    data['int_link'] = ""
    data['percent'] = (data['correct']/data['num'])*100
    return JsonResponse({'data': dumps(data, default=str)})


def schedule_interview(request, pk):
    if request.method == "POST":
        date_time_str = request.POST['date_time']
        # print(date_time_str)
        desired_datetime = timezone.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M")
        aware_datetime = timezone.make_aware(desired_datetime)
        ist_datetime = aware_datetime + timezone.timedelta(hours=5, minutes=30)
        applics = Application.objects.get(apply_id=request.POST['apply_id'])

        # + timezone.timedelta(hours=5, minutes=30)
        # print("hello",request.POST['user_id'])
        check = Interview.objects.filter(
            user_id=applics.user_id_id, eid=pk,apply_id=request.POST['apply_id'])
        if (len(check) != 0):
            check[0].int_link = request.POST['int_link']
            check[0].schedule_date = ist_datetime
            check[0].save()
            return JsonResponse({'m': 'A'})
        intval = Interview()
        intval.eid = Employer.objects.get(eid=pk)
        intval.user_id = JobSeeker.objects.get(user_id=applics.user_id_id)
        intval.int_link = request.POST['int_link']
        # print("hello",applics.apply_id)
        intval.apply_id = applics
        intval.schedule_date = ist_datetime
        intval.is_done = False
        intval.is_feedgiven = False
        intval.save()
        notif = Notifications()
        notif.notif_type = "I"
        notif.send_id = intval.eid.log_id
        notif.rece_id = intval.user_id.log_id
        notif.save()
        applics.status = 5
        applics.save()
        subject = "Interview scheduled by "+intval.eid.ename
        message = "Interview link: "+intval.int_link + \
            "\nDate: "+str(intval.schedule_date)
        receipt = [intval.user_id.log_id.email]
        send_emails(subject, message, receipt)
        return JsonResponse({'m': 'Y'})
    return JsonResponse({'m': 'X'})

def panel_request(request,pk):
    if request.method == "POST":
        inter = Interview.objects.get(int_id = request.POST['int_id'])
        # print(inter.int_id,request.POST['int_id'])
        inter.panel_req = 1
        inter.save()
        return JsonResponse({'m': 'Interview panel requested'})
        
def all_interviews(request, pk):
    if request.method == "POST":
        if 'act' in request.POST:
            if request.POST['act'] == "donall":
                for i in request.POST.getlist('ids[]'):
                    single_int = Interview.objects.get(int_id=i)
                    single_int.is_done = 1
                    single_int.save()
                return redirect('employer:all_interviews', pk=pk)
            for i in request.POST.getlist('ids[]'):
                Interview.objects.get(int_id=i).delete()
            return redirect('employer:all_interviews', pk=pk)
        Interview.objects.get(int_id=request.POST['int_id']).delete()
        return redirect('employer:all_interviews', pk=pk)
    all_ints = Interview.objects.filter(eid=pk).order_by('-schedule_date')
    final_ints = []
    for i in all_ints:
        single_int = {}
        single_int['int_id'] = i.int_id
        single_int['user_id'] = i.user_id.user_id
        single_int['name'] = i.user_id.name
        single_int['location'] = i.user_id.location
        single_int['date'] = i.schedule_date
        single_int['link'] = i.int_link
        single_int['isdone'] = i.is_done
        single_int['is_req'] = i.panel_req
        final_ints.append(single_int)
    GET_params = request.GET.copy()
    count = len(final_ints)
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(final_ints, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'interviews-employer.html', {'pk': pk, 'pe': page_obj, 'count': count})


def done(request, pk):
    if request.method == "POST":
        int_val = Interview.objects.get(int_id=request.POST['id'])
        int_val.is_done = 1
        int_val.save()
        return JsonResponse({'message': 'Y'})


def get_link(request, pk):
    int_val = Interview.objects.get(int_id=request.GET['int_id'])
    name = int_val.user_id.name
    if int_val.is_done == 0:
        return JsonResponse({'message': 'X', 'name': name})
    url = "http://localhost:8000/give_feedback/"+str(int_val.int_id)+"/"
    data = []
    if int_val.cand_feedback:
        data.append(int_val.cand_feedback)
    else:
        data.append(False)
    all_feeds = Feedback.objects.filter(int_id=request.GET['int_id'])
    if all_feeds:
        for i in all_feeds:
            data.append([i.name, i.emp_feedback])
    else:
        data.append(False)
    return JsonResponse({'message': 'Y', 'url': url, 'name': name, 'info': data})


def pending_actions(request, pk):
    applics = Application.objects.filter(eid=pk)
    GET_params = request.GET.copy()
    all_applics = []
    for i in applics:
        if i.status == 0 or i.status == 4:
            single_applic = {}
            single_applic['apply_id'] = i.apply_id
            single_applic['user_id'] = i.user_id.user_id
            single_applic['name'] = i.user_id.name
            single_applic['photo'] = ""
            if (i.user_id.photo):
                single_applic['photo'] = i.user_id.photo.url
            single_applic['location'] = i.user_id.location
            single_applic['title'] = i.job_id.title
            single_applic['job_location'] = i.job_id.location
            single_applic['apply_date'] = i.date_applied
            single_applic['status'] = i.status
            single_applic['jobid'] = i.job_id.jobid
            if i.status == 4:
                testinfo1 = TestInfo.objects.get(testinfoid=i.test.testinfoid)
                testuser1 = TestUser.objects.get(
                    test_id=testinfo1.test_id.test_id, user_id=i.user_id.user_id)
                single_applic['test_id'] = testuser1.testuser_id
                single_applic['results'] = (
                    int(testuser1.correct_answers)/int(testuser1.total_ques))*100
            else:
                single_applic['results'] = 0
            all_applics.append(single_applic)
    testinfo = TestInfo.objects.filter(eid=pk)
    count = len(applics)
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(all_applics, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'actions-employer.html', {'pk': pk, 'count': count, 'pe': page_obj, 'test': testinfo})


def logout(request, pk):
    employer = Login.objects.get(
        log_id=Employer.objects.get(eid=pk).log_id.log_id)
    employer.status = 0
    employer.save()
    request.session.flush()
    return redirect('main:index')

class JobMatcher:
    def __init__(self, jobseeker, job):
        self.jobseeker = jobseeker
        self.job = job
    
    

    def calculate_match_percentage(self):
        total_params = 5  
        matched_params = 0

        if self.jobseeker.skills and self.job.skills:
            job_skills = set(self.job.skills.lower().split(','))
            seeker_skills = set(self.jobseeker.skills.lower().split(','))
            if job_skills.intersection(seeker_skills):
                matched_params += 1

        # Check if location matches
        if self.job.location and self.jobseeker.location:
            if self.job.location.lower() == self.jobseeker.location.lower():
                matched_params += 1

        # Check if notice period matches
        if self.job.notice_period and self.jobseeker.notice_period:
            if self.job.notice_period.lower() == self.jobseeker.notice_period.lower():
                matched_params += 1

        # Check if Experience matches
        if self.jobseeker.experience and self.job.experience:
            if int(self.jobseeker.experience) >= int(self.job.experience):
                matched_params += 1

        # Check if expected salary matches
        # if self.jobseeker.expsal and self.job.basicpay:
        #     if self.jobseeker.expsal <= int(self.job.basicpay):
        #         matched_params += 1

        # Calculate match percentage
        match_percentage = (matched_params / total_params) * 100

        return match_percentage

    def get_matching_details(self):
        matching_details = {}

        # Check if skills match
        if self.jobseeker.skills and self.job.skills:
            job_skills = set(self.job.skills.lower().split(','))
            seeker_skills = set(self.jobseeker.skills.lower().split(','))
            matching_details['skills'] = {
                'match': list(job_skills.intersection(seeker_skills)),
                'not_match': list(job_skills.difference(seeker_skills))
            }
            

        # Check if location matches
        if self.job.location and self.jobseeker.location:
            matching_details['location'] = {
                'match': True if self.job.location.lower() == self.jobseeker.location.lower() else False
            }

        # Check if notice period matches
        if self.job.notice_period and self.jobseeker.notice_period:
            matching_details['notice_period'] = {
                'match': True if self.job.notice_period.lower() == self.jobseeker.notice_period.lower() else False
            }

        # Check if current salary matches
        if self.jobseeker.cursal and self.job.basicpay:
            matching_details['experience'] = {
                'match': True if int(self.jobseeker.experience) >= int(self.job.experience) else False
            }

        # Check if expected salary matches
        # if self.jobseeker.expsal and self.job.basicpay:
        #     matching_details['expected_salary'] = {
        #         'match': True if self.jobseeker.expsal <= int(self.job.basicpay) else False
        #     }

        return matching_details

def preprocess_text(text):
    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]

    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    preprocessed_text = ' '.join(words)
    return preprocessed_text


def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    try:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()
    except:
        pdf_text = ""
    return pdf_text
def suggest(request, pk):
    if request.method == "POST":
        send = False
        jobid = request.POST.get('jobid')
        if (jobid):
            try:
                job_ = Jobs.objects.get(jobid=jobid)
                if job_.status == 1 or job_.status == 3:
                    send = True
                job_.status = 5
                job_.save()
                matching_percentages = []
                for job_seeker in JobSeeker.objects.all():
                    if job_seeker.Resume and job_seeker.Resume.path and os.path.exists(job_seeker.Resume.path):
                        important_data_jobs = f"{job_.title} {job_.jobdesc} {job_.fnarea} {job_.skills} {job_.experience} {job_.basicpay} {job_.location} {job_.industry} {job_.ugqual} {job_.pgqual} {job_.profile} {job_.jobtype} {job_.requirements} {job_.responsibilities} {job_.notice_period}"
                        job_description = preprocess_text(important_data_jobs)

                        important_data_jobseeker = f"{job_seeker.location} {job_seeker.experience} {job_seeker.skills} {job_seeker.basic_edu} {job_seeker.master_edu} {job_seeker.other_qual} {job_seeker.cursal} {job_seeker.expsal} {job_seeker.notice_period}"
                        job_seeker_data = preprocess_text(important_data_jobseeker)
                        try:
                            resume_pdf_file = job_seeker.Resume.path
                            resume_text = extract_text_from_pdf(resume_pdf_file)
                        except:
                            pass
                        resume_text = preprocess_text(resume_text)
                        total_job_seeker_data = f"{job_seeker_data}{resume_text}"
                        vectorizer = CountVectorizer()

                        job_description_vector = vectorizer.fit_transform([job_description])
                        job_seeker_data_vector = vectorizer.transform([total_job_seeker_data])
                        cosine_sim_job_seeker = cosine_similarity(job_description_vector, job_seeker_data_vector)

                        job_matching_percentage = round(cosine_sim_job_seeker[0][0] * 100, 2)
                        job_matcher = JobMatcher(jobseeker=job_seeker, job=job_)
                        match_percentage = job_matcher.calculate_match_percentage()
                        total_matching_percentage = round((job_matching_percentage + match_percentage) / 2, 2)
                        matching_percentages.append((job_seeker.user_id, total_matching_percentage+20))
                        matching_percentages.sort(key=lambda x: x[1], reverse=True)

                top_matching_job_seekers = matching_percentages[:20]
                if(send):
                    email_list = []
                    for i in top_matching_job_seekers:
                        seek = JobSeeker.objects.get(user_id=i[0])
                        email_list.append(seek.log_id.email)
                    email_subject = "Job Alert"
                    message = "You are among top 20 best profiles for this job"
                    email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, email_list)
                    email.fail_silently = True
                    # email.content_subtype = "html"
                    email.send()
                email_subject = "Candidate suggestions"
                message = "Suggestions have been provided for {job_.title} job"
                email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [job_.eid.log_id.email])
                email.fail_silently = True
                    # email.content_subtype = "html"
                email.send()
                
                    
                # print(top_matching_job_seekers)
                serialized_list = json.dumps(top_matching_job_seekers)
                job_.suggestions = serialized_list
                job_.status = 4
                job_.save()
                
                return JsonResponse({'message': 'Candidate Suggestions are provided'})
            except Jobs.DoesNotExist:
                return JsonResponse({'message': 'Job not found'}, status=404)
        else:
            return JsonResponse({'message': 'Missing jobid'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
def requestCand(request,pk):
    if (request.method == "POST"):
        if(request.POST['jobid']):
            job = Jobs.objects.get(jobid=request.POST['jobid'])
            job.status = 6
            job.save()
            return JsonResponse({'message': 'Successfully Requested'}, status=200)
        else:
            return JsonResponse({'message': 'Try again'}, status=500)
    return JsonResponse({'message': 'Try again'}, status=500)

def resume_feedback(request,pk):
    if (request.method == "POST"):
        if(request.POST['jobid'] and request.POST['rating']):
            try:
                resfee = ResumeFeedback.objects.get(job_id=request.POST['jobid'])
                resfee.rating = request.POST['rating']
                resfee.save()
                return JsonResponse({'message': 'Successfully Updated'}, status=200)
            except ResumeFeedback.DoesNotExist:
                resfee = ResumeFeedback()
                resfee.job_id = Jobs.objects.get(jobid=request.POST['jobid'])
                resfee.rating = request.POST['rating']
                resfee.save()
                return JsonResponse({'message': 'Successfully submitted'}, status=200)
        else:
            return JsonResponse({'message': 'Try again'}, status=500)
    return JsonResponse({'message': 'Try again'}, status=500)


def all_templates(request, pk):
    if request.method == "POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                Templates.objects.get(template_id=i).delete()
            return redirect('employer:all_templates', pk=pk)
        Templates.objects.get(template_id=request.POST['temp_id']).delete()
        return redirect('employer:all_templates', pk=pk)
    templates = Templates.objects.filter(emp_id=pk)
    all_templates = []
    for i in templates:
        steps_count=len(TemplateSteps.objects.filter(template_id=i.template_id))
        single_template = {}
        single_template['temp_id'] = i.template_id
        single_template['temp_name'] = i.template_name
        single_template['temp_desc']=i.template_description
        single_template['created_date'] = i.created_date
        single_template['steps_count']=steps_count
        all_templates.append(single_template)
    sorted(all_templates, key=lambda i: i['created_date'])
    all_templates.reverse()
    GET_params = request.GET.copy()
    count = len(all_templates)
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(all_templates, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'templates-employer.html', {'pk': pk, 'pe': page_obj, 'count': count})

def create_temp(request, pk):
    if request.method == "POST":
        template=Templates()
        template.template_name=request.POST['name']
        template.template_description=request.POST['desc']
        template.emp_id=Employer.objects.get(eid=pk)
        template.save()
        return JsonResponse({'message': 'saved'})

def get_template(request, pk):
    template=Templates.objects.get(template_id=request.GET['temp_id'])
    step_temp=TemplateSteps.objects.filter(template_id=request.GET['temp_id']).order_by('step_order')
    final_data=[]
    for i in step_temp:
        mid_data=[]
        mid_data.append(i.step_order)
        mid_data.append(i.step_id.step_name)
        final_data.append(mid_data)
    return JsonResponse({'name': template.template_name, 'desc': template.template_description, 'date': template.created_date, 'info': final_data})

def edit_template(request, pk, pk2):
    template=Templates.objects.get(template_id=pk2)
    steps=TemplateSteps.objects.filter(template_id=pk2)
    if(request.method=="POST"):
        template.template_name=request.POST['templ_name']
        template.template_description=request.POST['templ_desc']
        template.save()
        return redirect('employer:edit_template', pk=pk, pk2=pk2)
    return render(request, 'edit-template-employer.html', {'pk': pk, 'pk2': pk2, 'template': template, 'steps': steps})

def schedule_temp(request, pk):
    if(request.method == "POST"):
        applics=Application.objects.get(apply_id=request.POST['appl_id'])
        applics.status=9
        applics.save()
        candidateassignment=CandidateTemplateAssignments()
        candidateassignment.candidate_id=applics.user_id
        candidateassignment.template_id=Templates.objects.get(template_id=request.POST['templ_id'])
        candidateassignment.current_step_order=1
        candidateassignment.application_id=applics
        candidateassignment.save()
        all_steps=TemplateSteps.objects.filter(template_id=request.POST['templ_id']).order_by('step_order')
        for i in all_steps:
            single_step=CandidateStepProgress()
            single_step.assignment_id=candidateassignment
            single_step.step_id=i.step_id
            single_step.is_completed=False
            single_step.save()
        return JsonResponse({'info': 'done'})
    
def get_temp_details(request, pk):
    cand_assign=CandidateTemplateAssignments.objects.get(candidate_id=request.GET['user_id'], application_id=request.GET['apply_id'])
    all_steps=CandidateStepProgress.objects.filter(assignment_id=cand_assign.assignment_id).order_by('progress_id')
    temp_data=[]
    curr_date=cand_assign.date_assigned
    for i in all_steps:
        single_data=[]
        single_data.append(i.step_id.step_name)
        single_data.append(i.is_completed)
        single_data.append(i.completion_date)
        single_data.append(curr_date)
        curr_date=curr_date+timedelta(days=1)
        temp_data.append(single_data)
    return JsonResponse({'temp_data': temp_data})


def get_all_steps(request, pk, pk2):
    all_steps=Steps.objects.filter(emp_id=pk)
    all_temp_steps=TemplateSteps.objects.filter(template_id=pk2)
    remaining_steps = all_steps.exclude(step_id__in=all_temp_steps.values_list('step_id', flat=True))
    if(request.method=="POST"):
        template_step=TemplateSteps()
        template_step.template_id=Templates.objects.get(template_id=pk2)
        template_step.step_id=Steps.objects.get(step_id=request.POST['step_id'])
        template_step.step_order=len(all_temp_steps)+1
        template_step.save()
        return JsonResponse({'message': 'added'})
    return JsonResponse({'info': dumps(list(remaining_steps.values()), default=str)})

def delastep(request, pk, pk2):
    if(request.method=="POST"):
        TemplateSteps.objects.get(template_id=pk2, step_id=request.POST['step_id']).delete()
        all_temp_steps=TemplateSteps.objects.filter(template_id=pk2).order_by('step_order')
        for i in range(0, len(all_temp_steps)):
            all_temp_steps[i].step_order=i+1
            all_temp_steps[i].save()
        return JsonResponse({'message': 'done'})

def all_steps(request, pk):
    if request.method == "POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                Steps.objects.get(step_id=i).delete()
            return redirect('employer:all_steps', pk=pk)
        Steps.objects.get(step_id=request.POST['step_id']).delete()
        return redirect('employer:all_steps', pk=pk)
    steps = Steps.objects.filter(emp_id=pk)
    all_steps = []
    for i in steps:
        single_step = {}
        single_step['step_id'] = i.step_id
        single_step['step_name'] = i.step_name
        single_step['step_desc'] = i.step_description
        single_step['created_date'] = i.created_date
        single_step['step_reso'] = i.step_resources
        single_step['step_task'] = i.step_tasks
        all_steps.append(single_step)
    sorted(all_steps, key=lambda i: i['created_date'])
    all_steps.reverse()
    GET_params = request.GET.copy()
    count = len(all_steps)
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    p = Paginator(all_steps, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'steps-employer.html', {'pk': pk, 'pe': page_obj, 'count': count})

def create_step(request, pk):
    if request.method == "POST":
        step=Steps()
        step.step_name=request.POST['name']
        step.step_description=request.POST['desc']
        step.step_resources=request.POST['reso']
        step.step_tasks=request.POST['task']
        step.emp_id=Employer.objects.get(eid=pk)
        step.save()
        return JsonResponse({'message': 'saved'})

def get_step(request, pk):
    step=Steps.objects.get(step_id=request.GET['step_id'])
    return JsonResponse({'name': step.step_name, 'desc': step.step_description, 'date': step.created_date, 'resources': step.step_resources, 'tasks': step.step_tasks})

def edit_step(request, pk):
    step=None
    if(request.method=="GET"):
        step=Steps.objects.filter(step_id=request.GET['step_id'])
    if(request.method=="POST"):
        step=Steps.objects.get(step_id=request.POST['step_id'])
        step.step_name=request.POST['name']
        step.step_description=request.POST['desc']
        step.step_resources=request.POST['reso']
        step.step_tasks=request.POST['task']
        step.save()
        return JsonResponse({'info': 'done'})
    return JsonResponse({'info': dumps(list(step.values()), default=str)})
from django.http import HttpResponseNotFound
def resume_link(request, pk):
    if request.method == "POST":
        try:
            seeker = JobSeeker.objects.get(user_id=request.POST.get('user_id'))
            link = seeker.Resume.url
            return JsonResponse({'link': link})
        except JobSeeker.DoesNotExist:
            return HttpResponseNotFound('Resume not found for this user')
    else:
        return JsonResponse({'error': 'Try POST method'})

def screening_questions(request, pk):
    if request.method == "POST":
        try:
            apply_id = request.POST.get('apply_id')
            if not apply_id:
                return JsonResponse({'error': 'No apply_id provided'})

            screening_answers = Application.objects.filter(apply_id=apply_id)
            if not screening_answers.exists():
                return JsonResponse({'Application not found'})

            screening_questions = ScreeningQuestions.objects.filter(job_id=screening_answers.first().job_id)
            if not screening_questions.exists():
                return JsonResponse({'Screening questions not found'})

            return JsonResponse({
                'screening_questions': list(screening_questions.values()),
                'screening_answers': list(screening_answers.values())
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Try using the POST method'})

def get_mocks(request):
    if request.method == "POST":
        job_id = request.POST.get('jobid') 

        if job_id:
            try:
                job_ = Jobs.objects.get(jobid=job_id)
                job_skills = job_.skills
                job_skills_list = job_skills.split(',')
                matching_mocktestinfo = MockTestInfo.objects.filter(tech__in=job_skills_list)
                return JsonResponse({'mocktests': matching_mocktestinfo.values()})

            except Jobs.DoesNotExist:
                return JsonResponse({'error': 'Job not found'}, status=404)

        return JsonResponse({'error': 'Missing or invalid jobid parameter'}, status=400)

def under_development(request, pk):
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'under_develop.html', {'pk': pk})
