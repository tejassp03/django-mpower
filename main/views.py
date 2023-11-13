from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Admin, JobSeeker, Login, Employer, ResumeAnalysis, Jobs, LikedJobs, Application, Interview, Feedback, Newsletter, Course, AllSkills, RoleDetails, Notifications, Seminars
import random
import re
import requests
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count
from django.template.loader import render_to_string
from jobster import settings
import pandas as pd
import time
from urllib.parse import urlparse
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
import random
from PIL import Image
from .Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import PyPDF2
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
import numpy as np
from itertools import groupby
from collections import defaultdict
from django.db.models import Count
import os
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse
# import plotly.express as px

from datetime import date, timedelta, datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain

from django.db.models import Q
from django.db.models import Max, Min

from json import dumps
import PyPDF2
import string

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ip2geotools.databases.noncommercial import DbIpCity

@csrf_exempt
def index(request):
    if request.method == 'POST':
        if 'location' in request.POST:
            longitude = request.POST['longitude']
            latitude = request.POST['latitude']
        user = Login.objects.filter(email=request.POST['c_email'])
        if (len(user) == 0):
            return JsonResponse({'message': 'X'})
        else:

            if (check_password(request.POST['c_pass'], user[0].password)):
                if (request.POST['user'] == 'candidate' and JobSeeker.objects.filter(log_id=user[0].log_id)):
                    jobseeker = JobSeeker.objects.get(log_id=user[0].log_id)
                    if ((jobseeker.phone == None or jobseeker.phone == "" or len(jobseeker.phone) <= 4) and (jobseeker.location == None or jobseeker.location == "") and (jobseeker.experience == None or jobseeker.experience == "") and (jobseeker.skills == None or jobseeker.skills == "") and (jobseeker.basic_edu == None or jobseeker.basic_edu == "") and (jobseeker.master_edu == None or jobseeker.master_edu == "") and (jobseeker.other_qual == None or jobseeker.other_qual == "") and (jobseeker.dob == None or jobseeker.dob == "") and (jobseeker.Resume == "" or jobseeker.Resume == None) and (jobseeker.photo == "" or jobseeker.photo == None)):
                        urlval = "/profile_completion/"+str(user[0].log_id)+"/"
                        return JsonResponse({'message': 'Y', 'url': urlval})
                    # return redirect('main:profilecompletion', pk=user[0].log_id)
                elif (request.POST['user'] == 'employer' and Employer.objects.filter(log_id=user[0].log_id)):
                    employer = Employer.objects.get(log_id=user[0].log_id)
                    if ((employer.etype == None or employer.etype == "") and (employer.industry == None or employer.industry == "") and (employer.address == None or employer.address == "") and (employer.pincode == None or employer.pincode == "") and (employer.executive == None or employer.executive == "") and (employer.phone == None or employer.phone == "" or len(employer.phone) <= 4) and (employer.location == None or employer.location == "") and (employer.profile == None or employer.profile == "") and (employer.logo == "" or employer.logo == None)):
                        urlval = "/emp_completion/"+str(user[0].log_id)+"/"
                        return JsonResponse({'message': 'Y', 'url': urlval})
                    
                else:
                    return JsonResponse({'message': 'X'})
                request.session['email'] = request.POST['c_email']
                request.session['password'] = user[0].password
                user[0].status = 1
                user[0].save()
                if (request.POST['user'] == 'candidate'):
                    empls = JobSeeker.objects.get(log_id=user[0].log_id)
                    request.session['name'] = empls.name
                    request.session['pk'] = empls.user_id
                    request.session['type'] = "c"
                    if (empls.photo):
                        request.session['photo'] = empls.photo.url
                    jobid = request.POST.get('jobid')
                    if jobid:
                        urlval = "/singlejob/"+jobid+"/"
                    else:
                        urlval = "/candidate/"+str(jobseeker.user_id)+"/"

                    # print(request.POST['jobid'])
                    return JsonResponse({'message': 'Y', 'url': urlval})
                else:
                    emp = Employer.objects.get(log_id=user[0].log_id)
                    request.session['name'] = emp.ename
                    request.session['pk'] = emp.eid
                    request.session['type'] = "e"
                    if (emp.logo):
                        request.session['photo'] = emp.logo.url
                    urlval = "/employer/"+str(emp.eid)+"/"
                    
                    return JsonResponse({'message': 'Y', 'url': urlval})
            else:
                return JsonResponse({'message': 'X'})
    
    jobs = Jobs.objects.all()
    typ = jobs.values('fnarea').annotate(
        Count('fnarea')).order_by('-fnarea__count')
    applics = Application.objects.values('job_id').annotate(
        Count('job_id')).order_by('-job_id__count')
    coms = jobs.values('eid').annotate(Count('eid')).order_by('-eid__count')
    vals = []
    co = 0
    try:
        user_ip = request.META.get('REMOTE_ADDR')
        url = f"https://ipinfo.io/{user_ip}/json"
        response = requests.get(url)

        data = response.json()
        user_city = data.get('city', 'City Not Found')
    except:
        pass
    seminars = Seminars.objects.all()
    seminar_distances = [(seminar, calculate_distance(seminar.city, user_city)) for seminar in seminars]
    seminar_distances.sort(key=lambda x: x[1])
    seminars_in_ascending_order = [seminar for seminar, _ in seminar_distances]

    for i in typ:
        if (co > 5):
            break
        single_val = {}
        single_val['fnarea'] = i['fnarea']
        single_val['count'] = i['fnarea__count']
        vals.append(single_val)
        co = co+1
    locations = jobs.order_by().values('location').distinct()
    titles = jobs.order_by().values('title').distinct()
    title = []
    locate = []
    jobs_info = []
    co = 0
    feature_jobs = jobs.order_by('-num_of_visits')
    for i in feature_jobs:
        if (co > 7):
            break
        single_j = {}
        sin = i
        single_j['fnarea'] = sin.fnarea
        single_j['title'] = sin.title
        single_j['location'] = sin.location
        single_j['type'] = sin.jobtype
        single_j['date'] = sin.postdate
        single_j['name'] = sin.eid.ename
        single_j['jobid'] = sin.jobid
        if (sin.eid.logo):
            single_j['logo'] = sin.eid.logo
        else:
            single_j['logo'] = None
        single_j['eid'] = sin.eid.eid
        jobs_info.append(single_j)
        co = co+1
    coms_info = []
    for i in coms:
        single_com = {}
        emp = Employer.objects.get(eid=i['eid'])
        single_com['name'] = emp.ename
        single_com['eid'] = emp.eid
        if (emp.logo):
            single_com['logo'] = emp.logo
        else:
            single_com['logo'] = None
        single_com['info'] = emp.profile
        single_com['count'] = i['eid__count']
        coms_info.append(single_com)
    for i in titles:
        title.append(i['title'])
    for i in locations:
        locate.append(i['location'])
    
    return render(request, 'index.html', {'locations': locations, 'titles': titles, 'title': dumps(title), 'vals': vals, 'jobs': jobs_info, 'coms': coms_info, 'loc': locate, 'total': len(jobs),'seminars':seminars_in_ascending_order})


def view_function(request):
    messages.add_message(request, messages.INFO, 'This is an info message')
    messages.add_message(request, messages.ERROR, 'This is an error message')
    return redirect('main:index')


def subscribe(request):
    if request.method == "POST":
        temp = Newsletter.objects.filter(email=request.POST['news_email'])
        if (len(temp) > 0):
            messages.error(request, 'Email already exists')
            return redirect('main:index')
        news = Newsletter()
        news.email = request.POST['news_email']
        news.save()
        messages.error(request, 'Subscription added')
        return redirect('main:index')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:candidates')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('main:user_login')
    else:
        return render(request, 'sign-in.html')


def admin_login(request):

    if 'type' in request.session and request.session['type'] == 'admin':
        return redirect('mpoweradmin:cdashboard', pk=request.session.get('pk'))
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['pass']
        user = Login.objects.filter(email=request.POST['email'])
        if (len(user) == 0):
            return JsonResponse({'message': 'X'})
        elif (check_password(request.POST['pass'], user[0].password)):
            # login(request, user)
            admin = Admin.objects.get(log_id=user[0].log_id)
            request.session['name'] = admin.aname
            request.session['pk'] = admin.aid
            request.session['type'] = "admin"
            return redirect('mpoweradmin:cdashboard', pk=admin.aid)
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('main:admin_login')
    else:
        return render(request, 'admin-login.html')


def register(request):
    if request.method == 'POST':
        if request.POST['name'] == "" or request.POST['email'] == "" or request.POST['password'] == "" or request.POST['conpass'] == "":
            messages.error(
                request, "Dont forget to fill out every field with the appropriate information")
            return redirect('main:index')
        all_login = Login.objects.filter(email=request.POST['email'])
        if (len(all_login) != 0):
            messages.success(
                request, 'Email address already in use, please enter some other email')
            return redirect('main:index')
        if (request.POST['password'] != request.POST['conpass']):
            messages.error(
                request, "Both your password and your confirmation password must be exactly same")
            return redirect('main:index')
        if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['password']):
            messages.error(request, "Please enter a valid password")
            return redirect('main:index')
        user = Login()
        user.email = request.POST['email']
        user.password = make_password(request.POST['password'])
        user.user_type = request.POST['user']
        user.save()
        if (request.POST['user'] == "candidate"):
            jobseeker = JobSeeker()
            rand_num = random.randint(0, 1000000000)
            jobseeker.user_id = rand_num
            jobseeker.log_id = user
            jobseeker.name = request.POST['name']
            jobseeker.save()
            messages.success(request, 'Successfully Registered')
            return redirect('main:profilecompletion', pk=user.log_id)
        elif (request.POST['user'] == "employer"):
            employer = Employer()
            rand_num = random.randint(0, 1000000000)
            employer.eid = rand_num
            employer.log_id = user
            employer.ename = request.POST['name']
            employer.save()
            messages.success(request, 'Successfully Registered')
            return redirect('main:emp_completion', pk=user.log_id)
        elif request.POST['user'] == "admin":
            admin = Admin()
            rand_num = random.randint(0, 1000000000)
            admin.aid = rand_num
            admin.log_id = user
            admin.aname = request.POST['name']
            admin.save()
            messages.success(request, 'Successfully Registered')
            return redirect('main:admin_completion', pk=user.log_id)

    return render(request, 'sign-up.html')


def admin_register(request):
    if request.method == 'POST':
        if request.POST['name'] == "" or request.POST['email'] == "" or request.POST['password'] == "" or request.POST['conpass'] == "":
            messages.error(
                request, "Dont forget to fill out every field with the appropriate information")
            return redirect('main:admin_register')
        all_login = Login.objects.filter(email=request.POST['email'])
        if (len(all_login) != 0):
            messages.success(
                request, 'Email address already in use, please enter some other email')
            return redirect('main:admin_register')
        if (request.POST['password'] != request.POST['conpass']):
            messages.error(
                request, "Both your password and your confirmation password must be exactly same")
            return redirect('main:admin_register')
        if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['password']):
            messages.error(request, "Please enter a valid password")
            return redirect('main:admin_register')
        user = Login()
        user.email = request.POST['email']
        user.password = make_password(request.POST['password'])
        user.user_type = request.POST['user']
        user.save()
        if (request.POST['user'] == "candidate"):
            jobseeker = JobSeeker()
            rand_num = random.randint(0, 1000000000)
            jobseeker.user_id = rand_num
            jobseeker.log_id = user
            jobseeker.name = request.POST['name']
            jobseeker.save()
            messages.success(request, 'Successfully Registered')
            return redirect('main:profilecompletion', pk=user.log_id)
        elif (request.POST['user'] == "employer"):
            employer = Employer()
            rand_num = random.randint(0, 1000000000)
            employer.eid = rand_num
            employer.log_id = user
            employer.ename = request.POST['name']
            employer.save()
            messages.success(request, 'Successfully Registered')
            return redirect('main:emp_completion', pk=user.log_id)
        elif request.POST['user'] == "admin":
            admin = Admin()
            rand_num = random.randint(0, 1000000000)
            admin.aid = rand_num
            admin.log_id = user
            admin.aname = request.POST['name']
            admin.email = request.POST['email']
            admin.save()
            messages.success(request, 'Successfully Registered')
            return redirect('main:admin_completion', pk=user.log_id)

    return render(request, 'admin-signup.html')


def blog(request):
    return render(request, 'blog-list-1.html')


def companies(request):
    return render(request, 'companies-list-3.html')


def candidates(request):
    return render(request, 'candidates-list-3.html')


def postjob(request):
    return render(request, 'company-dashboard-new-job.html')
 
def seminars(request):
    locs = request.GET.getlist('loc', None)
    locations = request.GET.getlist('location', None)
    titles = request.GET.getlist('title', None)
    datesort = request.GET.get('datesort',None)
    l_val = locs + locations
    d_val = datesort
    query = Q()
    if locs and any(locs):
        query &= Q(city__in=locs)

    if locations and any(locations):
        query &= Q(city__in=locations)

    if titles and any(titles):
        query &= Q(title__in=titles)
    sem = Seminars.objects.filter(query)
    if locs:
        sem = sem.filter(city__in=locs)

    if datesort:
        if datesort == 'newest':
            sem = sem.order_by('-date')  
        elif datesort == 'oldest':
            sem = sem.order_by('date')
    count = 0
    locations = []
    allsem = []
    
    titles_ = []
    all_locations = []
    for i in sem:
        single_location = {
            'location' : i.city
        }
        titles_.append(i.title)
        all_locations.append(i.city)
        singlesem = {
            'id': i.seminar_id,
            'title': i.title,
            'city': i.city,
            'poster': i.image.url,
            'date': i.date,
        }
        count = count+1
        locations.append(single_location)
        allsem.append(singlesem)

    p = Paginator(allsem, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'d':d_val,'l':l_val}
    print(context)
    return render(request, 'seminars.html', {'page_obj':page_obj,'pe': page_obj,'count':count,'locations':locations,'all_titles':titles_,'all_locations':all_locations,'context':context})


def findjobs(request):
    t_val = ""
    c_val = ""
    l_val = ""
    d_val = ""
    emp_sel = []
    exp_sel = []
    sal_sel = []
    wt_sel = []
    cat_sel = []
    loc_sel = []
    data = []
    exp = int(0)
    t_val = request.GET.get('title', '') or 'all'
    c_val = request.GET.get('category', '') or 'all'
    l_val = request.GET.get('location', '') or 'all'
    if (('title' not in request.GET) and ('category' not in request.GET) and ('location' not in request.GET)):
        jobs = Jobs.objects.all().order_by('-postdate')
    elif (t_val == "all" and l_val == "all" and c_val == "all"):
        jobs = Jobs.objects.all()
    elif (l_val == "all" and c_val == "all"):
        jobs = Jobs.objects.filter(title=request.GET['title'])
        # t_val = request.GET['title']
    elif (t_val == "all" and c_val == "all"):
        jobs = Jobs.objects.filter(location=request.GET['location'])
        # l_val = request.GET['location']
    elif (t_val == "all" and l_val == "all"):
        jobs = Jobs.objects.filter(fnarea=request.GET['category'])
        # c_val = request.GET['category']
    elif (t_val == "all"):
        jobs = Jobs.objects.filter(
            location=request.GET['location'], fnarea=request.GET['category'])
        # l_val = request.GET['location']
        # c_val = request.GET['category']
    elif (l_val == "all"):
        jobs = Jobs.objects.filter(
            title=request.GET['title'], fnarea=request.GET['category'])
        # t_val = request.GET['title']
        # c_val = request.GET['category']
    elif (c_val == "all"):
        jobs = Jobs.objects.filter(
            title=request.GET['title'], location=request.GET['location'])
        # t_val = request.GET['title']
        # l_val = request.GET['location']
    
    else:
        jobs = Jobs.objects.filter(
            title=request.GET['title'], location=request.GET['location'], fnarea=request.GET['category'])
        t_val = request.GET['title']
        l_val = request.GET['location']
        c_val = request.GET['category']
    
    if 'emp' in request.GET:
        jobs = jobs.filter(jobtype__in=request.GET.getlist('emp'))
        emp_sel = request.GET.getlist('emp')
    if 'exp' in request.GET:
        if int(request.GET['exp']) != 0:
            exp = int(request.GET['exp'])
            jobs = jobs.filter(experience__lte=exp)
            exp_sel = exp
        
    if 'sal' in request.GET:
        jobs = jobs.filter(basicpay__in=request.GET.getlist('sal'))
        sal_sel = request.GET.getlist('sal')

    if 'cat' in request.GET:
        jobs = jobs.filter(fnarea__in=request.GET.getlist('cat'))
        cat_sel = request.GET.getlist('cat')
    if 'loc' in request.GET:
        jobs = jobs.filter(location__in=request.GET.getlist('loc'))
        loc_sel = request.GET.getlist('loc')
    if 'datesort' in request.GET:
        d_val = request.GET['datesort']
        if (request.GET['datesort'] == "2"):
            jobs = jobs.reverse()
    GET_params = request.GET.copy()
    if ('page' in GET_params):
        last = GET_params['page'][-1]
        GET_params['page'] = last[0]
    count = len(jobs)
    companies = []
    for i in jobs:
        new_data = {}
        new_data['jobid'] = i.jobid
        new_data['title'] = i.title
        new_data['location'] = i.location
        new_data['experience'] = i.experience
        new_data['fnarea'] = i.fnarea
        new_data['postdat'] = i.postdate
        companies.append(Employer.objects.get(eid=i.eid.eid))
        em = Employer.objects.get(eid=i.eid.eid)
        new_data['eid'] = em.eid
        new_data['ename'] = em.ename
        new_data['logo'] = em.logo
        data.append(new_data)
    p = Paginator(data, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    categories = jobs.order_by().values('fnarea').distinct()
    locations = jobs.order_by().values('location').distinct()
    titles = jobs.order_by().values('title').distinct()
    jobtype = jobs.order_by().values('jobtype').distinct()
    emptype = jobs.order_by().values('experience').distinct()
    salary = jobs.order_by('basicpay').values('basicpay').distinct()
    countjob = []
    countemp = []
    countsal = []
    countloc = []
    all_jobs = Jobs.objects.all()
    all_titles = all_jobs.order_by().values('title').distinct()
    all_locations = all_jobs.order_by().values('location').distinct()
    all_cat = all_jobs.order_by().values('fnarea').distinct()
    for i in jobtype:
        countjob.append(len(jobs.filter(jobtype=i['jobtype'])))
    for i in emptype:
        countemp.append(len(jobs.filter(experience=i['experience'])))
    for i in salary:
        countsal.append(len(jobs.filter(basicpay=i['basicpay'])))
    for i in locations:
        countloc.append(len(jobs.filter(location=i['location'])))
    
    context = {'c': c_val, 'l': l_val, 't': t_val, 'd': d_val,
               'sel': emp_sel, 'eel': exp_sel, 'els': sal_sel,'wls':wt_sel,'cls':cat_sel,'lcs':loc_sel}
    if exp != 0:
        context['exp'] = exp
    locations_ = []
    for i in all_locations:
        locations_.append(i['location'])
    titles_ = []
    for i in all_titles:
        titles_.append(i['title'])
    return render(request, 'jobs.html', {'page_obj': page_obj, 'pe': page_obj, 'count': count, 'locations': locations,'countloc':countloc, 'titles': titles, 'categories': categories, 'GET_params': GET_params, 'jobtype': zip(jobtype, countjob), 'emptype': zip(emptype, countemp), 'saltype': zip(salary, countsal), 'context': context,'all_titles':titles_,'all_locations':locations_,'all_cats':all_cat})


def profile_completion(request, pk):
    if request.method == 'POST':
        flag1 = True
        for i in request.POST.getlist('experience'):
            if i != "":
                flag1 = False
        if (request.POST['mobile'] == "" and request.POST['address'] == "" and request.POST['dob'] == "" and request.POST['basic'] == "" and request.POST['master'] == "" and request.POST['other'] == "" and len(request.POST.getlist('skills')) == 0 and flag1 == True and len(request.FILES) == 0):
            messages.success(
                request, 'Please enter at least one of the fields')
            return redirect('main:profilecompletion', pk=pk)
        jobseeker = JobSeeker.objects.get(log_id=pk)
        jobseeker.phone = request.POST['code']+request.POST['mobile']
        jobseeker.location = request.POST['address']
        jobseeker.dob = request.POST['dob']
        jobseeker.basic_edu = request.POST['basic']
        jobseeker.master_edu = request.POST.get('master', None)
        jobseeker.other_qual = request.POST.get('other', None)
        jobseeker.cursal = request.POST.get('cursal', None)
        jobseeker.expsal = request.POST.get('expsal', None)
        notice_period_type = request.POST.get('notice_period_type', None)
        notice_period_time = request.POST.get('notice_period_time', None)
        jobseeker.role = request.POST.get('role',"")
        jobseeker.notice_period = f"{notice_period_time} {notice_period_type}"
        skills = request.POST.getlist('skills')
        all_skills = ""
        for i in skills:
            all_skills = all_skills+i+","
            
        experiences = request.POST.get('experience')
        jobseeker.skills = all_skills
        jobseeker.experience = experiences
         
        filev = None
        try:
            filev = request.FILES['resume']
            lst = filev._name.split(".")
            filev._name = str(pk)+"_"+jobseeker.name+"_Resume_"+filev._name
            jobseeker.Resume = filev
        except:
            filev = None
        try:
            filev = request.FILES['photo']
            lst = filev._name.split(".")
            filev._name = str(pk)+"_"+jobseeker.name+"_Photo_"+filev._name
            jobseeker.photo = filev
        except:
            filev = None
        
        jobseeker.save()
        loger = Login.objects.get(log_id=pk)
        request.session['email'] = loger.email
        request.session['password'] = loger.password
        empls = JobSeeker.objects.get(log_id=pk)
        request.session['name'] = empls.name
        request.session['pk'] = empls.user_id
        request.session['type'] = "c"
        resumeanalysis = ResumeAnalysis()
        resumeanalysis.actual_skills = all_skills
        resumeanalysis.jobseeker_id = jobseeker
        resumeanalysis.save()

        ########################EMAIL########################################
        matching_eid_list = []
        matching_job_titles = []
        matching_job_locations = []
        matching_company_names = []
        jobid_list = []

        all_jobs = Jobs.objects.all()

        for job in all_jobs:
            if job.skills:
                job_skills = job.skills.split(',')
        
                if any(skill.strip().lower() in all_skills.lower() for skill in job_skills):

                    matching_eid_list.append(job.eid_id)
            
                    matching_job_titles.append(job.title)
            
                    matching_job_locations.append(job.location)
                    jobid_list.append(job.jobid)

       

        matching_employers = Employer.objects.filter(eid__in=matching_eid_list)

        ename_dict = {employer.eid: employer.ename for employer in matching_employers}

        matching_company_names = [ename_dict[eid] for eid in matching_eid_list]
        

        matching_company_names = matching_company_names[:3]
        matching_job_titles = matching_job_titles[:3]
        matching_job_locations = matching_job_locations[:3]
        

        suggestions_match = True

        if len(matching_job_locations)==0 and len(matching_company_names)==0 and len(matching_job_titles) ==0:
            suggestions_match = False
        #####################################################################
        ### EMAIL############
        email_subject = "Registration Successfull"
        message = render_to_string('email.html', {
            'name': empls.name,
            'suggestions' :zip(matching_company_names,matching_job_titles,matching_job_locations,jobid_list),
            'suggestions_match' :suggestions_match,
            'cand_id':jobseeker.user_id
        })
        
        
        email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [loger.email])
        email.fail_silently = True
        email.content_subtype = "html"
        email.send()

        # if(empls.Resume):
        # 	analysis_object = ResumeAnalysis()
        # 	analysis_object.jobseeker_id = empls
        # 	resume_data = ResumeParser("media"+str(empls.Resume)).get_extracted_data()
        # 	data = ResumeParser('/path/to/resume/file').get_extracted_data()
        # 	if resume_data:
        # 		resume_text = pdf_reader("media/"+str(empls.Resume))
        # 		try:
        # 			analysis_object.no_of_pages=resume_data['no_of_pages']
        # 			# print(resume_data['name'], resume_data['email'], resume_data['mobile_number'], str(resume_data['no_of_pages']))
        # 		except:
        # 			print("!")
        # 		cand_level = ''
        # 		if resume_data['no_of_pages'] == 1:
        # 			cand_level = "Fresher"
        # 		elif resume_data['no_of_pages'] == 2:
        # 			cand_level = "Intermediate"
        # 		elif resume_data['no_of_pages'] >=3:
        # 			cand_level = "Experienced"
        # 		if(cand_level):
        # 			analysis_object.user_level=cand_level
        # 		if(resume_data['skills']):
        # 			final=""
        # 			for i in resume_data['skills']:
        # 				if(i!=""):
        # 					final=final+","+i
        # 			analysis_object.actual_skills=final
        # 		# print(resume_data['skills'])
        # 		ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
        # 		web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
        # 			'javascript', 'angular js', 'c#', 'flask']
        # 		android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
        # 		ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
        # 		uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']

        # 		recommended_skills = []
        # 		reco_field = ''
        # 		rec_course = ''
        # 		for i in resume_data['skills']:
        #             ## Data science recommendation
        # 			if i.lower() in ds_keyword:
        # 				# print(i.lower())
        # 				reco_field = 'Data Science'
        # 				recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
        # 				rec_course = course_recommender(ds_course)
        # 				break

        # 			## Web development recommendation
        # 			elif i.lower() in web_keyword:
        # 				# print(i.lower())
        # 				reco_field = 'Web Development'
        # 				recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
        # 				rec_course = course_recommender(web_course)
        # 				break

        # 			## Android App Development
        # 			elif i.lower() in android_keyword:
        # 				# print(i.lower())
        # 				reco_field = 'Android Development'
        # 				recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
        # 				rec_course = course_recommender(android_course)
        # 				break

        # 			## IOS App Development
        # 			elif i.lower() in ios_keyword:
        # 				# print(i.lower())
        # 				reco_field = 'IOS Development'
        # 				recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
        # 				rec_course = course_recommender(ios_course)
        # 				break

        # 			## Ui-UX Recommendation
        # 			elif i.lower() in uiux_keyword:
        # 				# print(i.lower())
        # 				reco_field = 'UI-UX Development'
        # 				recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
        # 				rec_course = course_recommender(uiux_course)
        # 				break
        # 		if(reco_field):
        # 			analysis_object.predicted_field=reco_field
        # 		if(recommended_skills):
        # 			final=""
        # 			for i in recommended_skills:
        # 				if(i!=""):
        # 					final=final+","+i
        # 			analysis_object.reco_skills=final
        # 		if(rec_course):
        # 			final=""
        # 			for i in rec_course:
        # 				if(i!=""):
        # 					final=final+","+i
        # 			analysis_object.reco_courses=final
        # 		resume_score = 0
        # 		recommendations=[]
        # 		if 'Objective' in resume_text:
        # 			resume_score = resume_score+20
        # 			recommendations.append('Awesome! You have added Objective')
        # 			# print("Objectives added good")
        # 		else:
        # 			recommendations.append('According to our recommendation please add your career objective, it will give your career intension to the Recruiters')
        # 			# print("According to our recommendation please add your career objective, it will give your career intension to the Recruiters")
        # 		if 'Declaration'  in resume_text:
        # 			resume_score = resume_score + 20
        # 			recommendations.append('Awesome! You have added Declaration')
        # 			# print("Declaration added good")
        # 		else:
        # 			recommendations.append('According to our recommendation please add Declaration. It will give the assurance that everything written on your resume is true and fully acknowledged by you')
        # 			# print("According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you")
        # 		if 'Hobbies' or 'Interests'in resume_text:
        # 			resume_score = resume_score + 20
        # 			recommendations.append('Awesome! You have added Hobbies')
        # 			# print("Hobbies or interests are added good")
        # 		else:
        # 			recommendations.append("According to our recommendation please add Hobbies. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.")
        # 			# print("According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.")
        # 		if 'Achievements' in resume_text:
        # 			resume_score = resume_score + 20
        # 			recommendations.append("Awesome! You have added Achievements")
        # 			# print("Achievements added good")
        # 		else:
        # 			recommendations.append("According to our recommendation please add Achievements. It will show that you are capable for the required position.")
        # 			# print("According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.")
        # 		if 'Projects' in resume_text:
        # 			resume_score = resume_score + 20
        # 			recommendations.append("Awesome! You have added Projects")
        # 			# print("Projects added good")
        # 		else:
        # 			recommendations.append("According to our recommendation please add Projects. It will show that you have done work related the required position or not.")
        # 			# print("According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.")
        # 		score = 0
        # 		for percent_complete in range(resume_score):
        # 			score +=1
        # 			time.sleep(0.1)
        # 		analysis_object.resume_score=score
        # 		final=""
        # 		for i in recommendations:
        # 			if(i!=""):
        # 				final=final+","+i
        # 		analysis_object.recommendations=final
        # 		analysis_object.save()
        # 		# print("Your resume score: ", score)

        if (empls.photo):
            request.session['photo'] = empls.photo.url
        loger.status = 1
        loger.save()
        return redirect("candidate:dashboard", pk=jobseeker.user_id)
    
    if (len(Login.objects.filter(log_id=pk, user_type="candidate")) == 0):
        return redirect('main:index')
    educat = Course.objects.all()
    allskills = AllSkills.objects.all()
    roledetails = RoleDetails.objects.all()
    return render(request, 'profile_completion.html', {'educat': educat, 'allskills': allskills,'roledetails':roledetails})


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text


def course_recommender(course_list):
    c = 0
    rec_course = []
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        rec_course.append(c_name)
        if c == 4:
            break
    return rec_course


def emp_completion(request, pk):
    if request.method == "POST":
        if (request.POST['code'] == "" and request.POST['mobile'] == "" and request.POST['etype'] == "" and request.POST['industry'] == "" and request.POST['executive'] == "" and len(request.FILES) == 0 and request.POST['address'] == "" and request.POST['pincode'] == "" and request.POST['location'] == "" and request.POST['profile'] == ""):
            messages.success(
                request, 'Please enter at least one of the fields')
            return redirect('main:eprofile', pk=pk)
        employer = Employer.objects.get(log_id=pk)
        employer.phone = request.POST['code']+request.POST['mobile']
        employer.etype = request.POST['etype']
        employer.industry = request.POST['industry']
        employer.executive = request.POST['executive']
        
        filev = None
        if 'logo' in request.FILES:
            filev = request.FILES['logo']
            lst = filev._name.split(".")
            filev._name = str(pk)+"_"+employer.ename+"_Logo_"+filev._name
            employer.logo = filev
        else:
            
            # static_folder_path = settings.STATIC_ROOT
            # images_folder_path = os.path.join(static_folder_path, "logo")
            images_folder_path = "/home/ec2-user/django-mpower/main/static/logo"
            image_files = os.listdir(images_folder_path)
            if image_files:
                file_bytes = None
                random_image_filename = random.choice(image_files)
                random_image_file_path = os.path.join(images_folder_path, random_image_filename)
                with open(random_image_file_path, "rb") as image_file:
                    file_bytes = image_file.read()
                filev = ContentFile(file_bytes)
                random_logo_name = str(pk)+"_"+employer.ename+"_Logo_"+random_image_filename
                employer.logo.save(random_logo_name, filev)
            
        employer.address = request.POST['address']
        employer.pincode = request.POST['pincode']
        employer.location = request.POST['location']
        employer.profile = request.POST['profile']
        employer.save()
        loger = Login.objects.get(log_id=pk)
        request.session['email'] = loger.email
        request.session['password'] = loger.password
        request.session['name'] = employer.ename
        request.session['pk'] = employer.eid
        request.session['type'] = "e"
        if (employer.logo):
            request.session['photo'] = employer.logo.url
        loger.status = 1
        loger.save()
        return redirect("employer:cdashboard", pk=employer.eid)
    
    if (len(Login.objects.filter(log_id=pk, user_type="employer")) == 0):
        return redirect('main:index')
    return render(request, 'emp_completion.html')


def admin_completion(request, pk):
    if request.method == "POST":
        if request.POST['arole'] == "" and request.POST['mobile'] == "":
            messages.success(
                request, 'Please enter at least one of the fields')
            return redirect('main:admin_completion', pk=pk)

        admin = Admin.objects.get(log_id=pk)
        admin.arole = request.POST['arole']
        admin.phone = request.POST['mobile']
        admin.save()

        loger = Login.objects.get(log_id=pk)
        request.session['email'] = loger.email
        request.session['password'] = loger.password
        request.session['name'] = admin.aname
        request.session['pk'] = admin.aid
        request.session['type'] = "admin"

        loger.status = 1
        loger.save()

        return redirect("mpoweradmin:cdashboard", pk=admin.aid)

    if len(Login.objects.filter(log_id=pk, user_type="admin")) == 0:
        return redirect('main:index')

    return render(request, 'admin_completion.html')


def returnvalue(phone):
    return str(phone) + str(datetime.date(datetime.now())) + "12345"


def get_otp(request, pk):
    if request.method == "GET":
        key = base64.b32encode(returnvalue(request.GET['phone']).encode())
        OTP = pyotp.TOTP(key, interval=30)
        return JsonResponse({'OTP': OTP.now()})
    return JsonResponse({'OTP': 'X'})


def verify_otp(request, pk):
    if (request.method == 'POST'):
        key = base64.b32encode(returnvalue(request.POST['phone']).encode())
        OTP = pyotp.TOTP(key, interval=30)
        if OTP.verify(int(request.POST['OTP'])):
            return JsonResponse({'message': 'Phone number verified'})
    return JsonResponse({'message': 'Please enter correct OTP'})


######################################################################################################



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
        if self.jobseeker.expsal and self.job.basicpay:
            if self.jobseeker.expsal <= int(self.job.basicpay):
                matched_params += 1

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
        if self.jobseeker.expsal and self.job.basicpay:
            matching_details['expected_salary'] = {
                'match': True if self.jobseeker.expsal <= int(self.job.basicpay) else False
            }

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

######################################################################################################################

def singleseminar(request,pk1):
    sem = Seminars.objects.get(seminar_id = pk1)
    singlesem= {}
    singlesem['title'] = sem.title
    singlesem['date'] = sem.date
    singlesem['address'] = sem.address
    singlesem['desc'] = sem.description
    singlesem['city'] = sem.city
    try:
        singlesem['poster'] = sem.image.url
    except:
        pass
    speakers = [speaker.strip() for speaker in sem.speaker.split(',')]

    return render(request,'singleseminar.html',{'seminar_details':singlesem,'speakers':speakers})

def singlejob(request, pk2):
    if request.method == "POST":
        job_id = Jobs.objects.get(jobid=pk2)
        user_id = JobSeeker.objects.get(user_id=request.session['pk'])

        # Check if the job already exists in the LikedJobs table
        liked_job = LikedJobs.objects.filter(
            job_id=job_id, user_id=user_id).first()

        if liked_job:
            # If the job exists, remove it from the LikedJobs table
            liked_job.delete()
        else:
            # If the job doesn't exist, add it to the LikedJobs table
            like = LikedJobs(job_id=job_id, user_id=user_id)
            like.save()
        return redirect('main:singlejob', pk2=pk2)
    jobdet = Jobs.objects.get(jobid=pk2)
    jobdet.num_of_visits = jobdet.num_of_visits+1
    jobdet.save()
    lik = False
    app_date = None
    companydet = Employer.objects.get(eid=jobdet.eid.eid)
    if 'pk' in request.session:
        liked = LikedJobs.objects.filter(
            job_id=pk2, user_id=request.session['pk'])
        if liked:
            lik = True
        applics = Application.objects.filter(
            job_id=pk2, user_id=request.session['pk'])
        if applics:
            app_date = applics[0].date_applied
    loger = Login.objects.get(log_id=companydet.log_id.log_id)
    skills = []
    skills_required = []
    for i in jobdet.skills.split("\n"):
        skills.append(i)
    requirements = []
    for i in jobdet.requirements.split("\n"):
        requirements.append(i)
    responsibilities = []
    for i in jobdet.responsibilities.split("\n"):
        responsibilities.append(i)
    quality = "Please login to check eligibility"
    if 'pk' in request.session:
        try:
            cand = JobSeeker.objects.get(user_id=request.session['pk'])
        except:
            cand = Employer.objects.get(eid=request.session['pk'])
            
        if cand.log_id.user_type == "employer":
            return render(request, 'singlejob.html', {'job_details': jobdet, 'company_details': companydet, 'liked': lik, 'loger': loger, 'skills': skills, 'requirements': requirements, 'responsibilities': responsibilities, 'date': app_date, 'score': 'X'})
        for i in skills:
            for j in cand.skills.split(","):
                if j not in i:
                    skills_required.append(i)
                    break
        try:
            pdfFileObj = open("static/media/"+str(cand.Resume), 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
        except:
            return render(request, 'singlejob.html', {'job_details': jobdet, 'company_details': companydet, 'liked': lik, 'loger': loger, 'skills': skills, 'requirements': requirements, 'responsibilities': responsibilities, 'date': app_date, 'score': 'Please submit your resume', 'skills_required': skills_required})
        num_pages = len(pdfReader.pages)
        count = 0
        text = ""
        while count < num_pages:
            pageObj = pdfReader.pages[count]
            count += 1
            text += pageObj.extract_text()
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        terms = {'Python Developer': ['black belt', 'capability analysis', 'control charts', 'doe', 'dmaic', 'fishbone',
                                      'gage r&r', 'green belt', 'ishikawa', 'iso', 'kaizen', 'kpi', 'lean', 'metrics',
                                      'pdsa', 'performance improvement', 'process improvement', 'quality',
                                      'quality circles', 'quality tools', 'root cause', 'six sigma',
                                      'stability analysis', 'statistical analysis', 'tqm'],
                 'Django Developer': ['automation', 'bottleneck', 'constraints', 'cycle time', 'efficiency', 'fmea',
                                      'machinery', 'maintenance', 'manufacture', 'line balancing', 'oee', 'operations',
                                      'operations research', 'optimization', 'overall equipment effectiveness',
                                      'pfmea', 'process', 'process mapping', 'production', 'resources', 'safety',
                                      'stoppage', 'value stream mapping', 'utilization'],
                 'React Developer': ['abc analysis', 'apics', 'customer', 'customs', 'delivery', 'distribution', 'eoq', 'epq',
                                     'fleet', 'forecast', 'inventory', 'logistic', 'materials', 'outsourcing', 'procurement',
                                     'reorder point', 'rout', 'safety stock', 'scheduling', 'shipping', 'stock', 'suppliers',
                                     'third party logistics', 'transport', 'transportation', 'traffic', 'supply chain',
                                     'vendor', 'warehouse', 'wip', 'work in progress'],
                 'NEXT Developer': ['administration', 'agile', 'budget', 'cost', 'direction', 'feasibility analysis',
                                    'finance', 'kanban', 'leader', 'leadership', 'management', 'milestones', 'planning',
                                    'pmi', 'pmp', 'problem', 'project', 'risk', 'schedule', 'scrum', 'stakeholders'],
                 'Project management': ['administration', 'agile', 'budget', 'cost', 'direction', 'feasibility analysis',
                                        'finance', 'kanban', 'leader', 'leadership', 'management', 'milestones', 'planning',
                                        'pmi', 'pmp', 'problem', 'project', 'risk', 'schedule', 'scrum', 'stakeholders'],
                 'Data analytics': ['analytics', 'api', 'aws', 'big data', 'busines intelligence', 'clustering', 'code',
                                    'coding', 'data', 'database', 'data mining', 'data science', 'deep learning', 'hadoop',
                                    'hypothesis test', 'iot', 'internet', 'machine learning', 'modeling', 'nosql', 'nlp',
                                    'predictive', 'programming', 'python', 'r', 'sql', 'tableau', 'text mining',
                                    'visualuzation'], }
        quality = 0
        for skill in skills:
            if skill in text:
                quality += 3
    # Check for other parameters such as location, position suitability, etc.
        if jobdet.location.lower() in text:
            quality += 3

        if jobdet.title.lower() in text:
            quality += 2
        quality += 2
        # if jobdet.basicpay:
        # 	if 'current salary' in text:
        # 		quality += 1

        # if jobdet['notice_period'].lower() in text:
        # 	quality += 1


    #######################################################################################
    if 'pk' in request.session:
        job = Jobs.objects.get(jobid=pk2)
        job_seeker = JobSeeker.objects.get(user_id=request.session['pk'])

        important_data_jobs = f"{job.title} {job.jobdesc} {job.fnarea} {job.skills} {job.experience} {job.basicpay} {job.location} {job.industry} {job.ugqual} {job.pgqual} {job.profile} {job.jobtype} {job.requirements} {job.responsibilities} {job.notice_period}"
        job_description = preprocess_text(important_data_jobs)

        important_data_jobseeker = f"{job_seeker.location} {job_seeker.experience} {job_seeker.skills} {job_seeker.basic_edu} {job_seeker.master_edu} {job_seeker.other_qual} {job_seeker.cursal} {job_seeker.expsal} {job_seeker.notice_period}"
        job_seeker_data = preprocess_text(important_data_jobseeker)

        resume_pdf_file = job_seeker.Resume.path
        resume_text = extract_text_from_pdf(resume_pdf_file)
        resume_text = preprocess_text(resume_text)
        total_job_seeker_data = f"{job_seeker_data}{resume_text}"
        vectorizer = CountVectorizer()

        job_description_vector = vectorizer.fit_transform([job_description])
        job_seeker_data_vector = vectorizer.transform([total_job_seeker_data])

        cosine_sim_job_seeker = cosine_similarity(job_description_vector, job_seeker_data_vector)

        job_matching_percentage = round(cosine_sim_job_seeker[0][0] * 100, 2)
    # print(f"Job Matching Percentage (Job Seeker Skills): {job_matching_percentage}%")
    #######################################################################################

    
    

        job_matcher = JobMatcher(jobseeker=job_seeker, job=job)
        match_percentage = job_matcher.calculate_match_percentage()
        matching_details = job_matcher.get_matching_details()
    
    
    # print(match_percentage)
    # print(matching_details)
    # context = {
    #     'match_percentage': match_percentage,
    #     'matching_details': matching_details,
    # }
        job_matching_percentage = round((job_matching_percentage+match_percentage)/2,2)
    else:
        job_matching_percentage = "Please login to check eligibility"
        matching_details = "No"
    return render(request, 'singlejob.html', {'job_details': jobdet, 'company_details': companydet, 'liked': lik, 'loger': loger, 'skills': skills, 'requirements': requirements, 'responsibilities': responsibilities, 'date': app_date, 'score': job_matching_percentage, 'skills_required': skills_required,'matching_details': matching_details})


    



def create_clusters_with_kmeans(job_seekers, num_clusters=5):
    all_skills = [', '.join(job_seeker.pass_to_list()) for job_seeker in job_seekers]

    vectorizer = CountVectorizer()
    skills_matrix = vectorizer.fit_transform(all_skills)

    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(skills_matrix)

    cluster_info = {}
    for i, job_seeker in enumerate(job_seekers):
        cluster_label = kmeans.labels_[i]
        email_id = job_seeker.log_id.email
        skills = job_seeker.pass_to_list()

        if cluster_label not in cluster_info:
            cluster_info[cluster_label] = {
                'email_ids': set(),
                'skills': set(),
            }

        if all(email_id not in cluster_info[other_cluster_label]['email_ids'] for other_cluster_label in cluster_info if other_cluster_label != cluster_label):
            cluster_info[cluster_label]['email_ids'].add(email_id)
        cluster_info[cluster_label]['skills'].update(skills)

        job_seeker.cluster_label = cluster_label

    return job_seekers, cluster_info




def calculate_similarity(cluster_skills, job_skills):
    skill_set = set(cluster_skills + job_skills)
    your_vector = [1 if skill in cluster_skills else 0 for skill in skill_set]
    job_vector = [1 if skill in job_skills else 0 for skill in skill_set]
    similarity_score = cosine_similarity([your_vector], [job_vector])
    return similarity_score[0][0]
def group_jobseekers_by_role():
    jobseekers_by_role = defaultdict(list)
    
    jobseekers = JobSeeker.objects.all()
    for jobseeker in jobseekers:
        jobseekers_by_role[jobseeker.role].append(jobseeker.log_id.email)
    
    return dict(jobseekers_by_role)



def daily_mail():
    jobs_queryset = Jobs.objects.all()
    email_subject = "Daily Job Recommendations"

    jobs_data = []
    for job in jobs_queryset:
        eid_id = job.eid_id
        title = job.title
        location = job.location
        skills = job.skills.split(',') if job.skills else []
        job_data = {
            'eid_id': eid_id,
            'title': title,
            'location': location,
            'skills': skills
        }
        jobs_data.append(job_data)
    grouped_jobs = {}
    for job_data in jobs_data:
        title = job_data['title']
        if title in grouped_jobs:
            grouped_jobs[title].append(job_data)
        else:
            grouped_jobs[title] = [job_data]
    
    role_email_list = []
    grouped_jobseekers = group_jobseekers_by_role()
    
   
    for role ,email_list in grouped_jobseekers.items():
        job_eid = []
        job_titles = []
        job_locations = []
        job_company = []
        
        if role is not None:
            job_list_for_role = grouped_jobs[role]
            for i in job_list_for_role:
                job_eid.append(i['eid_id'])
                job_titles.append(i['title'])
                job_locations.append(i['location'])
                
        if len(job_eid)>0:
            matching_employers = Employer.objects.filter(eid__in=job_eid)
            ename_dict = {employer.eid: employer.ename for employer in matching_employers}
            job_company = [ename_dict[eid] for eid in job_eid]
            message = render_to_string('daily-email.html', {  
                'suggestions': zip(job_company, job_titles, job_locations),
                'suggestions_match': True
            })
            role_email_list.extend(email_list)
            email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, email_list)
            email.fail_silently = True
            email.content_subtype = "html"
            email.send()


    
    all_job_seekers = JobSeeker.objects.exclude(log_id__email__in=role_email_list)
    clustered_job_seekers, cluster_info = create_clusters_with_kmeans(all_job_seekers)

    

    for cluster_label, info in cluster_info.items():
        cluster_skill_list = []
        cluster_email_list = []
        recommanded_company_names = []
        for skill in info['skills']:
            cluster_skill_list.append(skill)
        for email_id in info['email_ids']:
            cluster_email_list.append(email_id)
        jobs_with_scores = [(job['eid_id'], job['title'], job['location'], calculate_similarity(cluster_skill_list, job['skills'])) for job in jobs_data]
        sorted_jobs = sorted(jobs_with_scores, key=lambda x: x[3], reverse=True)
        top_5_recommended_jobs = sorted_jobs[:5]
        recommended_eids = [eid for eid, _, _, _ in top_5_recommended_jobs]
        recommended_titles = [title for _, title, _, _ in top_5_recommended_jobs]
        recommended_locations = [location for _, _, location, _ in top_5_recommended_jobs]

        
        matching_employers = Employer.objects.filter(eid__in=recommended_eids)
        ename_dict = {employer.eid: employer.ename for employer in matching_employers}
        recommanded_company_names = [ename_dict[eid] for eid in recommended_eids]
        
        message = render_to_string('daily-email.html', {
            'name': 'Aditya',  
            'suggestions': zip(recommanded_company_names, recommended_titles, recommended_locations),
            'suggestions_match': True
        })

        email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, cluster_email_list)
        email.fail_silently = True
        email.content_subtype = "html"
        email.send()
        
        


def singlecompany(request, pk2):
    cominfo = Employer.objects.get(eid=pk2)
    jobs = Jobs.objects.filter(eid=cominfo.eid).order_by('-postdate')
    return render(request, 'singlecompany.html', {'cominfo': cominfo, 'jobs': jobs})


def get_job(request):
    if (request.method == "GET"):
        job = Jobs.objects.get(jobid=request.GET['id'])
        return JsonResponse({'name': job.title, 'id': job.jobid})
    if (request.method == "POST"):
        applic = Application()
        applic.user_id = JobSeeker.objects.get(user_id=request.session['pk'])
        applic.status = 0
        applic.job_id = Jobs.objects.get(jobid=request.POST['id'])
        applic.eid = applic.job_id.eid
        applic.why_desc = request.POST['whyhire']
        applic.date_applied = timezone.localtime() 
        # + timedelta(hours=5, minutes=30)
        applic.save()
        return JsonResponse({'message': 'Y'})


def give_feedback(request, pk):
    if request.method == "POST":
        int_val = Interview.objects.get(int_id=pk)
        applics = Application.objects.get(apply_id = int_val.apply_id.apply_id)
        eid_id = applics.eid.eid
        applics.status = 7
        applics.save()
        int_val.is_feedgiven = 1
        int_val.save()
        try:
            existing_feedback = Feedback.objects.get(int_id=int_val)
            if existing_feedback:
                existing_feedback.rating = request.POST['rating']
                existing_feedback.emp_feedback = request.POST['feedback']
                existing_feedback.name = request.POST['name']
                existing_feedback.save()
                messages.error(request, "Feedback successfully Modified!")
                return redirect('employer:all_interviews', pk=eid_id)
        except:
            feedback = Feedback()
            feedback.int_id = int_val
            feedback.rating = request.POST['rating']
            feedback.emp_feedback = request.POST['feedback']
            feedback.name = request.POST['name']
            feedback.save()
        notif = Notifications()
        notif.notif_type = "F"
        notif.send_id = applics.eid.log_id
        notif.rece_id = applics.user_id.log_id
        notif.job_id = applics.job_id
        notif.save()
        messages.error(request, "Feedback successfully recorded!")
        return redirect('employer:all_interviews', pk=eid_id)
    try:
        int_val = Interview.objects.get(int_id=pk)
    except:
        int_val = Interview.objects.get(apply_id=pk)
    data = {}
    data['name'] = int_val.user_id.name
    data['location'] = int_val.user_id.location
    data['title'] = int_val.user_id.role
    if int_val.user_id.photo:
        data['photo'] = int_val.user_id.photo
    return render(request, 'give_feedback.html', {'data': data})


def give_feed(request, pk):
    if request.method == "POST":
        int_val = Interview.objects.get(int_id=pk)
        int_val.cand_feedback = request.POST['feedback']
        int_val.save()
        return redirect("main:index")
    int_val = Interview.objects.get(int_id=pk)
    data = {}
    data['ename'] = int_val.eid.ename
    data['location'] = int_val.eid.location

    if int_val.eid.logo:
        data['logo'] = int_val.eid.logo.url
    return render(request, 'give_feed.html', {'data': data})
class MyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.email}-{timestamp}"

my_token_generator = MyTokenGenerator()
def token_is_valid(email_encoded,token, timestamp):
    email_ = urlsafe_base64_decode(email_encoded)

    try:
        email = urlsafe_base64_decode(email_encoded).decode('utf-8')
        
        user = Login.objects.get(email=email)
        if my_token_generator.check_token(user, token):
            timestamp_datetime = timezone.datetime.fromisoformat(timestamp)
            
            time_difference = timezone.now() - timestamp_datetime
            
            if time_difference <= timedelta(minutes=10):
                return True
    
    except (TypeError, ValueError, OverflowError, Login.DoesNotExist):
        pass
    
    return False

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = Login.objects.filter(email=email).first()
        if user:
            email_encoded = urlsafe_base64_encode(email.encode())
            token = my_token_generator.make_token(user)
            timestamp = timezone.now().isoformat()
            parsed_url = urlparse(request.build_absolute_uri())
            main_url = f"{parsed_url.scheme}://{parsed_url.netloc}" 
            reset_link = reverse('main:password_reset_confirm', args=[email_encoded,token, timestamp])
            subject = 'Password Reset Request'
            message = f'Click the following link to reset your password: {main_url}{reset_link}'
            from_email = 'your_email@example.com'
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
            return JsonResponse({'message': 'Password reset link sent successfully'})
        return JsonResponse({'error': 'User with this email does not exist'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def password_reset_confirm(request,email_encoded, token, timestamp):
    if not token_is_valid(email_encoded,token, timestamp):
        return HttpResponse('Invalid or expired password reset link.')
    return render(request, 'password-reset.html',{'email_encoded':email_encoded})

def password_reset(request):
    if request.method == "POST":
        email_encoded = request.POST['email_encoded']
        email_ = urlsafe_base64_decode(email_encoded).decode('utf-8')
        user = get_object_or_404(Login, email=email_)

        if request.POST['fnew'] != request.POST['cnew']:
            return JsonResponse({'message': 'Both your password and your confirmation password must be exactly the same'})
        
        if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['fnew']):
            return JsonResponse({'message': 'Please enter a valid password'})        
        user.password = make_password(request.POST['fnew'])
        user.save()
        request.session['password'] = None
        return JsonResponse({'message': 'Password changed successfully'})

def calculate_distance(origin,destination):

    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={origin}"
        response = requests.get(url)
        data = response.json()
        origin_coords = (float(data[0]['lat']), float(data[0]['lon']))

        url = f"https://nominatim.openstreetmap.org/search?format=json&q={destination}"
        response = requests.get(url)
        data = response.json()
        destination_coords = (float(data[0]['lat']), float(data[0]['lon']))

        from math import radians, sin, cos, sqrt, atan2
        lat1, lon1 = map(radians, origin_coords)
        lat2, lon2 = map(radians, destination_coords)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        radius = 6371

        distance = round(radius * c, 2)
        # print(distance, "km")

        return distance
    except Exception as e:
        # return JsonResponse({'error': str(e)})
        
        return "Error"


def about_us(request):
    return render(request,'about-us.html')
def pricing(request):
    return render(request,'pricing.html')
def contact_us(request):
    return render(request,'contact-us.html')
def faqs(request):
    return render(request,'faqs.html')
def signup(request):
    return render(request,'sign-up.html')
def signin(request):
    return render(request,'sign-in.html')
# def error_404_view(request, exception):
#     return render(request, '404.html')
