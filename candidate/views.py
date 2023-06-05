import os
from django.shortcuts import render, redirect
from main.models import *
from json import dumps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import re
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain
from django.template import RequestContext

from datetime import date, timedelta, datetime
import heapq

import pyotp
import base64
import PyPDF2
import string
import spacy
from jobster.settings import BASE_DIR


# Create your views here.
def dashboard(request, pk):
    context = JobSeeker.objects.get(user_id=pk)
    applics = Application.objects.filter(user_id=pk)
    profile = ProfileVisits.objects.filter(user_id=pk)
    userobj = JobSeeker.objects.get(user_id=pk)
    num_notif = Notifications.objects.filter(rece_id=context.log_id).order_by('-datetime')
    all_notis=[]
    threads = Threads.objects.filter(receiver=userobj.log_id)
    countunmess=0
    recent_mess=[]
    testuser=TestUser.objects.filter(user_id=pk)
    popupmess=[]
    for i in testuser:
        if i.answers:
            continue
        else:
            testinfo=TestInfo.objects.get(test_id=i.test_id.test_id)
            ans="You have a pending test scheduled by "+testinfo.eid.ename+" (test name "+testinfo.test_name+")"
            popupmess.append(ans)
    int_vals=Interview.objects.filter(user_id=pk, is_done=1)
    for i in int_vals:
        if i.cand_feedback:
            continue
        else:
            ans="Please provide your feedback for the interview with "+i.eid.ename+"\n Link: http://localhost:8000/give_feed/"+str(i.int_id)
            popupmess.append(ans)
    for i in threads:
        mess=Messages.objects.filter(msg_id=i.msg_id, receiver_user=userobj.log_id.log_id).order_by("-date")
        if(len(mess)>0):
            countunmess=countunmess+len(mess.filter(is_read=0))
            tempval=[]
            tempval.append(mess[0].date)
            tempval.append(mess[0].body)
            compan=Employer.objects.get(log_id=mess[0].sender_user.log_id)
            tempval.append(compan.ename)
            tempval.append(compan.logo)
            recent_mess.append(tempval)
    recent_mess.sort(reverse=True)
    recent_mess_temp=[]
    idx=min(4, len(recent_mess))
    for i in range(0, idx):
        recent_mess_temp.append(recent_mess[i])
    count=0
    for i in num_notif:
        single_notis={}
        single_notis['notif_type']=i.notif_type
        single_notis['datetime']=i.datetime
        emp=Employer.objects.get(log_id=i.send_id)
        single_notis['ename']=emp.ename
        single_notis['eid']=emp.eid
        single_notis['log_id']=emp.log_id.log_id
        all_notis.append(single_notis)
        count=count+1
        if(count>10):
            break
    all_applics=[]
    for i in applics:
        singappli={}
        job=Jobs.objects.get(jobid=i.job_id.jobid)
        singappli['jobid']=job.jobid
        singappli['title']=job.title
        singappli['fnarea']=job.fnarea
        singappli['location']=job.location
        singappli['jobtype']=job.jobtype
        com=Employer.objects.get(eid=job.eid.eid)
        singappli['ename']=com.ename
        singappli['logo']=com.logo
        all_applics.append(singappli)


    visits = ProfileVisits.objects.filter(user_type="c", user_id=pk)
    applics_chart=[]
    applics_7=[]
    applics_30=[]
    applics_60=[]
    applics_90=[]
    applics_365=[]
    counts=[]
    cou=0

    visits_chart=[]
    visits_7=[]
    visits_30=[]
    visits_60=[]
    visits_90=[]
    visits_365=[]
    countsv=[]
    couv=0
    for i in range(0, 365):
        d=date.today()-timedelta(days=i)
        temp = applics.filter(date_applied__year=d.year, date_applied__month=d.month, date_applied__day=d.day)
        n=len(temp)
        heapq.heappush(applics_chart, (-1*(n), n, d))
        cou=cou+n
        temp = visits.filter(visiting_time__year=d.year, visiting_time__month=d.month, visiting_time__day=d.day)
        n=len(temp)
        heapq.heappush(visits_chart, (-1*(n), n, d))
        couv=couv+n
        if(len(applics_chart)==7):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_7.append([applics_chart[j][2], applics_chart[j][1]])
                visits_7.append([visits_chart[j][2], visits_chart[j][1]])
        if(len(applics_chart)==30):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_30.append([applics_chart[j][2], applics_chart[j][1]])
                visits_30.append([visits_chart[j][2], visits_chart[j][1]])
        if(len(applics_chart)==60):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_60.append([applics_chart[j][2], applics_chart[j][1]])
                visits_60.append([visits_chart[j][2], visits_chart[j][1]])
        if(len(applics_chart)==90):
            counts.append(cou)
            countsv.append(couv)
            for j in range(0, 7):
                applics_90.append([applics_chart[j][2], applics_chart[j][1]])
                visits_90.append([visits_chart[j][2], visits_chart[j][1]])
        if(len(applics_chart)==364):
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
    charts_context={}
    charts_context['pastsev']=dumps([item[1] for item in applics_7])
    charts_context['dates']=dumps([item[0] for item in applics_7], default=str)
    charts_context['count_7']=dumps(counts[0])
    charts_context['pastthi']=dumps([item[1] for item in applics_30])
    charts_context['dates30']=dumps([item[0] for item in applics_30], default=str)
    charts_context['count_30']=dumps(counts[1])
    charts_context['pastsix']=dumps([item[1] for item in applics_60])
    charts_context['dates60']=dumps([item[0] for item in applics_60], default=str)
    charts_context['count_60']=dumps(counts[2])
    charts_context['pastnin']=dumps([item[1] for item in applics_60])
    charts_context['dates90']=dumps([item[0] for item in applics_60], default=str)
    charts_context['count_90']=dumps(counts[3])
    charts_context['pastyea']=dumps([item[1] for item in applics_365])
    charts_context['dates365']=dumps([item[0] for item in applics_365], default=str)
    charts_context['count_365']=dumps(counts[4])

    charts_context['vpastsev']=dumps([item[1] for item in visits_7])
    charts_context['vdates']=dumps([item[0] for item in visits_7], default=str)
    charts_context['vcount_7']=dumps(countsv[0])
    charts_context['vpastthi']=dumps([item[1] for item in visits_30])
    charts_context['vdates30']=dumps([item[0] for item in visits_30], default=str)
    charts_context['vcount_30']=dumps(countsv[1])
    charts_context['vpastsix']=dumps([item[1] for item in visits_60])
    charts_context['vdates60']=dumps([item[0] for item in visits_60], default=str)
    charts_context['vcount_60']=dumps(countsv[2])
    charts_context['vpastnin']=dumps([item[1] for item in visits_90])
    charts_context['vdates90']=dumps([item[0] for item in visits_90], default=str)
    charts_context['vcount_90']=dumps(countsv[3])
    charts_context['vpastyea']=dumps([item[1] for item in visits_365])
    charts_context['vdates365']=dumps([item[0] for item in visits_365], default=str)
    charts_context['vcount_365']=dumps(countsv[4])
    return render(request, 'dashboard-candidate.html', {'user': context, 'applications': all_applics, 'pk': pk, 'profile': profile, 'notifics': all_notis, 'messcount': countunmess, 'charts': charts_context, 'recent': recent_mess_temp, 'pending': popupmess})


def jobapp(request, pk):
    jobinfo = Jobs.objects.filter(jobid=request.GET['jobid'])
    employer = Employer.objects.filter(eid=jobinfo[0].eid.eid)
    email = Login.objects.get(log_id=employer[0].log_id.log_id)
    email = {'email': email.email}
    image=""
    if(employer[0].logo):
        image = str(employer[0].logo.url)
    cand=JobSeeker.objects.get(user_id=pk)
    actual_skills=jobinfo[0].skills.split("\n")
    user_skills=cand.skills.split(",")
    skills_required=[]
    for i in actual_skills:
        for j in user_skills:
            if j not in i:
                skills_required.append(i)
                break
    quality=0
    try: 
        pdfFileObj = open("media/"+str(cand.Resume),'rb')  
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    except:
        return JsonResponse({'logo': image, 'info': dumps(list(jobinfo.values()), default=str), 'company': dumps(list(employer.values())), 'emai': dumps(email), 'score': "Please submit resume to check eligibility", 'skills_required': skills_required})
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    text = text.lower()
    text = re.sub(r'\d+','',text)
    text = text.translate(str.maketrans('','',string.punctuation))
    terms = {'Python Developer':['black belt','capability analysis','control charts','doe','dmaic','fishbone',
                            'gage r&r', 'green belt','ishikawa','iso','kaizen','kpi','lean','metrics',
                            'pdsa','performance improvement','process improvement','quality',
                            'quality circles','quality tools','root cause','six sigma',
                            'stability analysis','statistical analysis','tqm'],      
        'Django Developer':['automation','bottleneck','constraints','cycle time','efficiency','fmea',
                                'machinery','maintenance','manufacture','line balancing','oee','operations',
                                'operations research','optimization','overall equipment effectiveness',
                                'pfmea','process','process mapping','production','resources','safety',
                                'stoppage','value stream mapping','utilization'],
        'React Developer':['abc analysis','apics','customer','customs','delivery','distribution','eoq','epq',
                        'fleet','forecast','inventory','logistic','materials','outsourcing','procurement',
                        'reorder point','rout','safety stock','scheduling','shipping','stock','suppliers',
                        'third party logistics','transport','transportation','traffic','supply chain',
                        'vendor','warehouse','wip','work in progress'],
        'NEXT Developer':['administration','agile','budget','cost','direction','feasibility analysis',
                            'finance','kanban','leader','leadership','management','milestones','planning',
                            'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
        'Project management':['administration','agile','budget','cost','direction','feasibility analysis',
                    'finance','kanban','leader','leadership','management','milestones','planning',
                    'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
        'Data analytics':['analytics','api','aws','big data','busines intelligence','clustering','code',
                        'coding','data','database','data mining','data science','deep learning','hadoop',
                        'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                        'predictive','programming','python','r','sql','tableau','text mining',
                        'visualuzation'],}
    quality = 0
    for area in terms.keys():
        if area.lower() == jobinfo[0].title.lower():
            for word in terms[area]:
                if word in text:
                    quality +=1
            break
    return JsonResponse({'logo': image, 'info': dumps(list(jobinfo.values()), default=str), 'company': dumps(list(employer.values())), 'emai': dumps(email), 'score': quality, 'skills_required': skills_required})


def edit_profile(request, pk):
    context = JobSeeker.objects.get(user_id=pk)
    skills = context.skills.split(",")
    experience = ExperienceJob.objects.filter(user_id=pk)
    education = Education.objects.filter(user_id=pk)
    for i in skills:
        if i=="":
            skills.remove(i)
    if(request.method=="POST"):
        jobseeker=JobSeeker.objects.get(user_id=pk)
        jobseeker.name=request.POST['name']
        jobseeker.title=request.POST['title']
        jobseeker.location=request.POST['location']
        # jobseeker.phone=request.POST['phone']
        jobseeker.about=request.POST['about']
        filev=None
        try:
            filev=request.FILES['photo']
            lst=filev._name.split(".")
            filev._name=str(pk)+"_"+jobseeker.name+"_Photo_"+filev._name
            if jobseeker.photo:
                jobseeker.photo.delete()
            jobseeker.photo = filev
        except:
            filev=None
        finder=Login.objects.get(email=request.session['email'])
        finder.email=request.POST['email']
        finder.save()
        jobseeker.save()
        request.session['email']=request.POST['email']
        request.session['name']=request.POST['name']
        ss_info=JobSeeker.objects.get(user_id=pk)
        if(ss_info.photo):
            request.session['photo']=ss_info.photo.url
        return redirect('candidate:edit', pk=pk)
    return render(request, 'profile-candidate.html', {'user': context, 'pk': pk, 'log': request.session['email'], 'skills': skills, 'experience': experience, 'education': education})

def returnvalue(phone):
	return str(phone) + str(datetime.date(datetime.now())) + "12345"

def get_o(request, pk):
	if request.method == "GET":
		key = base64.b32encode(returnvalue(request.GET['phone']).encode())
		OTP = pyotp.TOTP(key,interval = 30)
		return JsonResponse({'OTP': OTP.now()})
	return JsonResponse({'OTP': 'X'})

def post_o(request, pk):
	if(request.method=='POST'):
		key = base64.b32encode(returnvalue(request.POST['phone'][3:]).encode())
		OTP = pyotp.TOTP(key,interval = 30)
		if OTP.verify(int(request.POST['OTP'])):
			return JsonResponse({'message': 'Phone number verified'})
	return JsonResponse({'message': 'Please enter correct OTP'})

def upd_phone(request, pk):
    if request.method=="POST":
        jobseek=JobSeeker.objects.get(user_id=pk)
        jobseek.phone=request.POST['phone']
        jobseek.save()
        return JsonResponse({'message': 'x'})

def add_skill(request, pk):
    if(request.method=="POST"):
        user=JobSeeker.objects.get(user_id=pk)
        user.skills=user.skills+","+request.POST['skill']
        if len(user.skills)>=2:
            if user.skills[0]==",":
                user.skills=user.skills[1:len(user.skills)]
            if user.skills[-1]==",":
                user.skills=user.skills[0:len(user.skills)-1]
        user.save()
    return redirect('candidate:edit', pk=pk)

def add_exp(request, pk):
    if(request.method=="POST"):
        exp = ExperienceJob()
        user=JobSeeker.objects.get(user_id=pk)
        exp.user_id=user
        exp.job_title=request.POST['title']
        exp.company=request.POST['company']
        exp.time_period=request.POST['time_period']
        exp.description=request.POST['description']
        exp.save()
    return redirect('candidate:edit', pk=pk)

def add_edu(request, pk):
    if(request.method=="POST"):
        edu = Education()
        user=JobSeeker.objects.get(user_id=pk)
        edu.user_id=user
        edu.title=request.POST['title']
        edu.school=request.POST['school']
        edu.time_period=request.POST['period_edu']
        edu.description=request.POST['desc']
        edu.save()
    return redirect('candidate:edit', pk=pk)

def delete_skill(request, pk):
    if request.method == "POST":
        skill=JobSeeker.objects.get(user_id=pk)
        skills=skill.skills.split(',')
        for i in skills:
            if i==request.POST['val']:
                skills.remove(i)
        final=""
        for i in skills:
            if i!="":
             final=final+","+i
        if(len(final)>0):
            if(final[0]==","):
                final=final[1:len(final)]
            if(final[-1]==","):
                final=final[0:len(final)-1]
        skill.skills=final
        skill.save()
    return redirect('candidate:edit', pk=pk)

def delete_exp(request, pk):
    if request.method == "POST":
        exp = ExperienceJob.objects.get(exp_id=request.POST['id'])
        exp.delete()
    return redirect('candidate:edit', pk=pk)

def delete_edu(request, pk):
    if request.method == "POST":
        edu = Education.objects.get(edu_id=request.POST['id'])
        edu.delete()
    return redirect('candidate:edit', pk=pk)

def edit_exp(request, pk):
    exp=None
    if(request.method=="GET"):
        exp = ExperienceJob.objects.filter(exp_id=request.GET['expid'])
    else:
        exp = ExperienceJob.objects.filter(exp_id=request.POST['expid'])
    if request.method=="POST":
        if(len(exp)>0):
            exp[0].job_title=request.POST['job_title']
            exp[0].company=request.POST['company']
            exp[0].time_period=request.POST['time_period']
            exp[0].description=request.POST['description']
            exp[0].save()
        return redirect('candidate:edit', pk=pk)
    return JsonResponse({'info': dumps(list(exp.values()), default=str)})

def edit_edu(request, pk):
    edu=None
    if(request.method=="GET"):
        edu = Education.objects.filter(edu_id=request.GET['eduid'])
    else:
        edu = Education.objects.filter(edu_id=request.POST['eduid'])
    if request.method=="POST":
        if(len(edu)>0):
            edu[0].title=request.POST['title']
            edu[0].school=request.POST['school']
            edu[0].time_period=request.POST['time_period']
            edu[0].description=request.POST['description']
            edu[0].save()
        return redirect('candidate:edit', pk=pk)
    return JsonResponse({'info': dumps(list(edu.values()), default=str)})

def thread(request, pk):
    if request.method == "POST":
        jobseek=JobSeeker.objects.get(user_id=pk)
        threads=Threads.objects.get(sender=request.POST['sender'], receiver=jobseek.log_id.log_id)
        request.session['thread']=threads.msg_id
        return JsonResponse({'url': ""})

def inbox(request, pk):
    shower=""
    if 'thread' in request.session:
        shower=request.session['thread']
        del request.session['thread']
    if(request.method=="POST"):
        thread=Threads.objects.get(msg_id=request.POST['employer'])
        message=Messages()
        message.msg_id=thread
        message.sender_user=Login.objects.get(email=request.session['email'])
        message.receiver_user=Login.objects.get(log_id=thread.sender.log_id)
        message.body=request.POST['message']
        message.save()
        urlval="candidate/"+str(pk)+"/inbox"
        return JsonResponse({'message': 'Y', 'url': urlval})
    user=Login.objects.get(email=request.session['email'])
    threads=Threads.objects.filter(receiver=user.log_id)
    temp_threads=[dumps(list(threads.values()), default=str)]
    messages=[]
    temp_messages=[]
    empls=[]
    temp_empls=[]
    first=None
    recent_mess=[]
    for i in threads:
        mess=Messages.objects.filter(msg_id=i.msg_id)
        messages.append(dumps(list(mess.values()), default=str))
        temp_messages.append(mess)
        logs_info=Employer.objects.get(log_id=i.sender.log_id)
        logs_info2=Employer.objects.filter(log_id=i.sender.log_id)
        temp_empls.append(logs_info)
        empls.append(dumps(list(logs_info2.values()), default=str))
        recent=mess.order_by('-date')
        c_u=len(mess.filter(is_read=0))
        if(len(recent)>0):
            if(str(recent[0].sender_user)==str(user.log_id)):
                recent_mess.append(["c", recent[0].body, recent[0].date, c_u])
            else:
                recent_mess.append(["e", recent[0].body, recent[0].date, c_u])
        else:
            recent_mess.append(["x", None, i.date, None, None])
    if(temp_empls):
        first=temp_empls[0]
    # print(threads)
    # print(temp_empls)
    # print(recent_mess)
    return render(request, 'inbox-candidate.html', {'pk': pk, 'threads': threads, 'first': first ,'mess': messages, 'thre': temp_threads, 'm': temp_messages, 'emp': empls, 'initial': zip(threads, temp_empls, recent_mess), 'shower': shower})


def under_development(request, pk):
    return render(request, 'under_development.html', {'pk': pk})


def employer(request, pk, pk2):
    candidate = JobSeeker.objects.all()
    return render(request, 'employer.html', {'candidates': candidate, 'pk': pk, 'pk2': pk2})

def startconver(request, pk, pk2, pk3):
    threads = Threads.objects.filter(sender=Login.objects.get(log_id=pk2), receiver=Login.objects.get(log_id=pk3))
    sender = Employer.objects.get(log_id=pk2)
    receiver = JobSeeker.objects.get(log_id=pk3)
    messages=[]
    if(len(threads)==1):
        messages=Messages.objects.filter(msg_id=threads[0].msg_id)
    if(len(threads)==0):
        thread = Threads()
        thread.sender = Login.objects.get(log_id=pk2)
        thread.receiver = Login.objects.get(log_id=pk3)
        thread.save()
        thread=Threads.objects.get(sender=Login.objects.get(log_id=pk2), receiver=Login.objects.get(log_id=pk3))
        messages=Messages.objects.filter(msg_id=thread.msg_id)
        return redirect('candidate:startconver', pk=pk, pk2=pk2, pk3=pk3)
    return render(request, 'startconver.html', {'candidate': receiver, 'pk': pk, 'pk2': pk2, 'pk3': pk3, 'messages': messages})

def send(request, pk, pk2, pk3):
    if request.method == "POST" and request.POST['message']:
        threads = Threads.objects.get(sender=Login.objects.get(log_id=pk2), receiver=Login.objects.get(log_id=pk3))
        message=Messages()
        message.msg_id=threads
        message.sender_user=Login.objects.get(log_id=pk2)
        message.receiver_user=Login.objects.get(log_id=pk3)
        message.body=request.POST['message']
        message.save()
        return redirect('candidate:startconver', pk=pk, pk2=pk2, pk3=pk3)
    return redirect('candidate: startconver', pk=pk, pk2=pk2, pk3=pk3)

def sendfromcand(request, pk):
    if(request.method=="POST"):
        thread=Threads.objects.get(msg_id=request.POST['employer'])
        message=Messages()
        message.msg_id=thread
        message.sender_user=Login.objects.get(email=request.session['email'])
        message.receiver_user=Login.objects.get(log_id=thread.sender.log_id)
        message.body=request.POST['message']
        message.save()
        urlval="candidate/"+str(pk)+"/inbox"
        user=Login.objects.get(email=request.session['email'])
        threads=Threads.objects.filter(receiver=user.log_id)
        temp_threads=[dumps(list(threads.values()), default=str)]
        messages=[]
        temp_messages=[]
        for i in threads:
            mess=Messages.objects.filter(msg_id=i.msg_id)
            messages.append(dumps(list(mess.values()), default=str))
            temp_messages.append(mess)
        notif=Notifications()
        notif.notif_type="M"
        notif.send_id=Login.objects.get(email=request.session['email'])
        notif.rece_id=Login.objects.get(log_id=thread.sender.log_id)
        notif.save()
        return JsonResponse({'message': 'Y', 'url': "", 'id': request.POST['employer'], 'thre': temp_threads, 'm': messages})

def fetchmess(request, pk):
    if request.GET['employer']=="":
        return JsonResponse({'message': 'X'})
    user=Login.objects.get(email=request.session['email'])
    threads=Threads.objects.filter(receiver=user.log_id)
    temp_threads=[dumps(list(threads.values()), default=str)]
    messages=[]
    temp_messages=[]
    mess_all=[]
    urlval=""
    count=0
    ind_unread=[]
    rece=[]
    for i in threads:
        mess=Messages.objects.filter(msg_id=i.msg_id, receiver_user=user.log_id, is_read=False)
        si=len(mess)
        count=si+count
        ind_unread.append([i.msg_id, si])
        messages.append(dumps(list(mess.values()), default=str))
        temp_messages.append(mess)
        mess=Messages.objects.filter(msg_id=i.msg_id)
        n=len(mess)
        if(n>0):
            if(mess[n-1].sender_user.log_id==user.log_id):
                rece.append({'msg_id': i.msg_id, 'body': "You: "+mess[len(mess)-1].body, 'type': "e"})
            else:
                comname=Employer.objects.get(log_id=mess[n-1].sender_user.log_id)
                rece.append({'msg_id': i.msg_id, 'body': comname.ename+": "+mess[len(mess)-1].body, 'type': "c"})
        mess_all.append(dumps(list(mess.values()), default=str))
    comp_thread=Threads.objects.get(msg_id=request.GET['employer'])
    comp_log=Login.objects.get(log_id=comp_thread.sender.log_id)
    thread=dumps(list(Threads.objects.filter(msg_id=request.GET['employer']).values()), default=str)
    messa=dumps(list(Messages.objects.filter(msg_id=request.GET['employer'], receiver_user=user.log_id, is_read=False).values()), default=str)
    company=dumps(list(Employer.objects.filter(log_id=comp_log).values()), default=str)
    urlval=Employer.objects.filter(log_id=comp_log)[0].logo.url
    return JsonResponse({'message': 'Y', 'url': "", 'mess': messages, 'thre': temp_threads, 'count': count, 'thread': thread, 'company': company ,'messa': messa, 'all_mess': mess_all, 'image': urlval, 'unread': dumps(ind_unread), 'rece': dumps(rece)})

def seenmes(request, pk):
    loger=Login.objects.get(email=request.session['email'])
    if(request.method=="POST"):
        if request.POST['employer']=="":
            return JsonResponse({'message': 'X'})
        messages=Messages.objects.filter(msg_id=request.POST['employer'], receiver_user=loger.log_id, is_read=False)
        Messages.objects.filter(msg_id=request.POST['employer'], receiver_user=loger.log_id, is_read=False).update(is_read=True)
        for i in messages:
            i.is_read=True
            i.save()
        return JsonResponse({'message': 'Y'})


def resume(request, pk):
    data={}
    jobseek=JobSeeker.objects.filter(user_id=pk)
    urlval=None
    if jobseek:
        urlval=jobseek[0].Resume.url
    if request.method=="POST":
        print(request.FILES)
        jobseek[0].Resume.delete()
        filev=request.FILES['resume']
        lst=filev._name.split(".")
        filev._name=str(pk)+"_"+jobseek[0].name+"_Resume_"+filev._name
        jobseek[0].Resume = filev
        jobseek[0].save()
        return redirect('candidate:resume', pk=pk)
    try:
        context=ResumeAnalysis.objects.get(jobseeker_id=pk)
        data['score']=context.resume_score
        data['num']=context.no_of_pages
        data['predicted']=context.predicted_field
        data['user']=context.user_level
        data['skills']=context.actual_skills
        data['reco_skills']=context.reco_skills
        data['reco_courses']=context.reco_courses
        data['recommendations']=context.recommendations
        data['upload']="Y"
    except:
        data['score']=0
        data['num']=0
        data['predicted']=""
        data['user']=""
        data['skills']=""
        data['reco_skills']=""
        data['reco_courses']=""
        data['recommendations']=""
        data['upload']="N"
    return render(request, 'resume.html', {'pk': pk, 'context': data, 'url': urlval})

def count_inbox(request, pk):
    # user=JobSeeker.objects.get(user_id=pk)
    # num_mess=Threads.objects.filter(receiver=user.log_id, has_unread=1)
    loger=Login.objects.get(email=request.session['email'])
    countval=len(Messages.objects.filter(receiver_user=loger.log_id, is_read=False))
    return JsonResponse({'count': countval})


def change(request, pk):
    if request.method=="POST":
        user=Login.objects.get(email=request.session['email'])
        if(check_password(request.POST['old'], user.password)):
            if request.POST['new']!=request.POST['cnew']:
                messages.error(request, "Both your password and your confirmation password must be exactly same")
                return redirect('candidate:change', pk=pk)
            if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['new']):
                messages.error(request, "Please enter a valid password")
                return redirect('candidate:change', pk=pk)
            if(request.POST['old']==request.POST['new']):
                messages.error(request, "Old and new password cant be same")
                return redirect('candidate:change', pk=pk)
            user.password=make_password(request.POST['new'])
            user.save()
            request.session['password']=user.password
            messages.success(request, 'Password changed successfully')
            return redirect('candidate:change', pk=pk)
        else:
            messages.error(request, "Please enter correct old password")
            return redirect('candidate:change', pk=pk)
    return render(request, 'password-candidate.html', {'pk': pk})

def favjobs(request, pk):
    if request.method=="POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                LikedJobs.objects.filter(like_id=i).delete()
            return redirect('candidate:favjobs', pk=pk)
        LikedJobs.objects.filter(like_id=request.POST['like_id']).delete()
        return redirect('candidate:favjobs', pk=pk)
    all_fav = LikedJobs.objects.filter(user_id=pk).order_by('-likedate')
    all_det = []
    for i in all_fav:
        data={}
        data['like_id']=i.like_id
        data['likedate']=i.likedate
        job=Jobs.objects.get(jobid=i.job_id.jobid)
        data['title']=job.title
        data['jobid']=job.jobid
        data['location']=job.location
        data['fnarea']=job.fnarea
        data['jobtype']=job.jobtype
        emp=Employer.objects.get(eid=job.eid.eid)
        data['ename']=emp.ename
        data['eid']=emp.eid
        all_det.append(data)
    count=len(all_fav)
    GET_params = request.GET.copy()
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(all_det, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'favjobs-candidate.html', {'pk': pk, 'fav': page_obj, 'count': count, 'pe': page_obj, 'GET_params': GET_params})

def notifications(request, pk):
    loger=Login.objects.get(email=request.session['email'])
    notifs=Notifications.objects.filter(rece_id=loger.log_id).order_by('-datetime')
    nots=[]
    for i in notifs:
        i.readed=True
        i.save()
        request.session['notifnum']=0
        single_notif={}
        single_notif['notif_id']=i.notif_id
        single_notif['notif_type']=i.notif_type
        single_notif['datetime']=i.datetime
        com = Employer.objects.get(log_id=i.send_id)
        single_notif['eid']=com.eid
        single_notif['ename']=com.ename
        single_notif['log_id']=com.log_id.log_id
        nots.append(single_notif)
    count=len(notifs)
    GET_params = request.GET.copy()
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(nots, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'notification-candidate.html', {'pk': pk, 'notif': page_obj, 'count': count})


def applications(request, pk):
    if request.method=="POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                Application.objects.filter(apply_id=i).delete()
            return redirect('candidate:applications', pk=pk)
        Application.objects.filter(apply_id=request.POST['apply_id']).delete()
        return redirect('candidate:applications', pk=pk)
    applics=Application.objects.filter(user_id=pk).order_by("-date_applied")
    count=len(applics)
    all_app=[]
    for i in applics:
        app={}
        app['apply_id']=i.apply_id
        job=Jobs.objects.get(jobid=i.job_id.jobid)
        app['jobid']=job.jobid
        app['title']=job.title
        app['location']=job.location
        app['fnarea']=job.fnarea
        app['jobtype']=job.jobtype
        app['date_applied']=i.date_applied
        com=Employer.objects.get(eid=job.eid.eid)
        app['ename']=com.ename
        app['eid']=com.eid
        all_app.append(app)
    GET_params = request.GET.copy()
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(all_app, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'applications-candidate.html', {'pk': pk, 'all_app': page_obj, 'GET_params': GET_params, 'count': count})

def suggestions(request, pk):
    user_skills=JobSeeker.objects.get(user_id=pk)
    user_skills=user_skills.skills.lower().split(",")
    jobs_skills=Jobs.objects.all()
    all_suggest=[]
    for i in jobs_skills:
        # print(user_skills)
        # print(i.skills.lower().split(","))
        if i.skills:
            if(any(j in user_skills for j in i.skills.lower().split("\n"))):
                sugg = {}
                sugg['jobid']=i.jobid
                sugg['title']=i.title
                sugg['location']=i.location
                sugg['fnarea']=i.fnarea
                sugg['jobtype']=i.jobtype
                sugg['date_applied']=i.postdate
                emp=Employer.objects.get(eid=i.eid.eid)
                sugg['ename']=emp.ename
                sugg['eid']=emp.eid
                all_suggest.append(sugg)
    count=len(all_suggest)
    GET_params = request.GET.copy()
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(all_suggest, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'suggestions-candidate.html', {'pk': pk, 'fav': page_obj, 'count': count, 'pe': page_obj, 'GET_params': GET_params})

def company(request, pk):
    cominfo=Employer.objects.filter(eid=request.GET['eid'])
    email=Login.objects.get(log_id=cominfo[0].log_id.log_id)
    email = {'email': email.email}
    image=""
    if(cominfo[0].logo):
        image = str(cominfo[0].logo.url)
    cover=""
    if(cominfo[0].cover):
        cover = str(cominfo[0].cover.url)
    visit=ProfileVisits()
    visit.e_id=cominfo[0]
    visit.user_id=JobSeeker.objects.get(user_id=pk)
    visit.user_type="e"
    visit.save()
    notif=Notifications()
    notif.notif_type="V"
    notif.send_id=Login.objects.get(email=request.session['email'])
    notif.rece_id=Login.objects.get(log_id=cominfo[0].log_id.log_id)
    notif.save()
    return JsonResponse({'info': dumps(list(cominfo.values()), default=str), 'emai': dumps(email), 'logo': image, 'cover': cover})

def tests(request, pk):
    test=TestUser.objects.filter(user_id=pk)
    all_test=[]
    for i in test:
        if i.answers:
            single_test={}
        else:
            single_test={}
            single_test['test_id']=i.test_id.test_id
            testinfo=TestInfo.objects.get(test_id=i.test_id.test_id)
            single_test['name']=testinfo.test_name
            single_test['timelimit']=testinfo.time_limit
            emp=Employer.objects.get(eid=testinfo.eid.eid)
            single_test['eid']=emp.eid
            single_test['ename']=emp.ename
            all_test.append(single_test)
    count=len(all_test)
    GET_params = request.GET.copy()
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(all_test, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'tests-candidate.html', {'pk': pk, 'all_app': page_obj, 'count': count})

def attempt(request, pk, pk2):
    testinfo=TestInfo.objects.get(test_id=pk2)
    testques=TestQues.objects.filter(testinfoid=testinfo.testinfoid)
    name=testinfo.test_name
    all_ques=[]
    for i in testques:
        single_ques={}
        single_ques['ques_id']=i.ques_id
        single_ques['question']=i.ques_name
        single_ques['opt1']=i.option1
        single_ques['opt2']=i.option2
        single_ques['opt3']=i.option3
        single_ques['opt4']=i.option4
        all_ques.append(single_ques)
    return render(request, 'attempt-employer.html', {'pk': pk, 'pk2': pk2, 'test': all_ques, 'name': name})

def submit(request, pk):
    if request.method=="POST":
        usertest=TestUser.objects.get(user_id=pk, test_id=request.POST['testid'])
        testinfo=TestInfo.objects.get(test_id=request.POST['testid'])
        testques=TestQues.objects.filter(testinfoid=testinfo.testinfoid)
        ans=request.POST.getlist('answers[]')
        usertest.total_ques=len(testques)
        count=0
        str_ans=""
        for i, j in zip(testques, ans):
            str_ans=str_ans+str(j)+','
            if i.correct == int(j):
                count=count+1
        usertest.correct_answers=count
        usertest.answers=str_ans
        usertest.date=datetime.now()
        usertest.save()
        applics=Application.objects.get(user_id=pk, test=testinfo)
        applics.status=4
        applics.save()
        notif=Notifications()
        notif.notif_type="T"
        notif.send_id=Login.objects.get(email=request.session['email'])
        notif.rece_id=testinfo.eid.log_id
        notif.testuser_id=usertest
        notif.save()
    return JsonResponse({'message': "submitted"})

def interviews(request, pk):
    inter=Interview.objects.filter(user_id=pk).order_by('schedule_date')
    all_inters=[]
    for i in inter:
        single_inter={}
        single_inter['int_id']=i.int_id
        single_inter['eid']=i.eid.eid
        single_inter['ename']=i.eid.ename
        single_inter['date']=i.schedule_date
        single_inter['link']=i.int_link
        single_inter['location']=i.eid.location
        single_inter['isdone']=i.is_done
        if(i.eid.logo):
            single_inter['logo']=i.eid.logo
        else:
            single_inter['logo']=""
        all_inters.append(single_inter)
    count=len(all_inters)
    GET_params = request.GET.copy()
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(all_inters, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'interviews-candidate.html', {'pk': pk, 'pe': page_obj, 'count': count})

def get_interview(request, pk):
    inter=Interview.objects.get(eid=request.GET['eid'], user_id=pk)
    data={}
    data['date']=inter.schedule_date
    data['link']=inter.int_link
    data['ename']=inter.eid.ename
    return JsonResponse({'info': dumps(data, default=str)})

def feed_get(request, pk):
    inter=Interview.objects.get(eid=request.GET['eid'], user_id=pk)
    data={}
    data['comname']=inter.eid.ename
    data['is_cand_done']=False
    if inter.cand_feedback:
        data['is_cand_done']=True
        data['feed_cand']=inter.cand_feedback
    else:
        ans="Please provide your feedback for the interview with "+inter.eid.ename+"\n Link: http://localhost:8000/give_feed/"+str(inter.int_id)
        data['feed_cand']=ans
    data['feed_received']=[]
    feeds=Feedback.objects.filter(int_id=inter.int_id)
    for i in feeds:
        data['feed_received'].append(i.emp_feedback)
    return JsonResponse({'info': data})

def job_change(request, pk):
    cand=JobSeeker.objects.get(user_id=pk)
    text=cand.skills 
    key=[]
    value=[]
    str1="candidate\output\model-best"
    model_path = os.path.join(BASE_DIR, str1)
    nlp = spacy.load(model_path)
    doc = nlp(text)
    for ent in doc.ents:
        key.append(ent.label_)
        value.append(ent.text)
    print("Key:", key)  # Print the value of 'key'
    print("Value:", value)
    Dict = {key[i]: value[i] for i in range(len(key))}
    SKILLS = Dict["JOB ROLE"].lower().rstrip(",").split(",")
    print(SKILLS)
    Dict.update(SKILLS=SKILLS)
    text = Dict["JOB ROLE"]
    len_user_list = len(text)
    all_jobs=Jobs.objects.all()
    set1=set(text)
    final_jobs=[]
    for i in all_jobs:
        if i.skills is not None:
            set2=set(i.skills.lower().split("\n"))
            print(set1, " ", set2)
            if set1 & set2:
                final_jobs.append(i)

    
    jobs = []
    if not final_jobs:
        for i in final_jobs:
            job_skills = i.skills.lower().split("\n")
            match = len([k for k , val in enumerate(job_skills) if val in text])
            total_len = len(job_skills) + len_user_list
            jobs.append([i, match/total_len])
        sorted(jobs, key = lambda x: x[1], reverse=True)
        final_vals=[]
        for i in jobs:
            temp_dic={}
            temp_dic['eid']=i[0].eid.eid
            temp_dic['jobid']=i[0].jobid
            temp_dic['rank']=float(i[1])*100
            temp_dic['title']=i[0].title
            temp_dic['location']=i[0].location
            temp_dic['ename']=i[0].eid.ename
            temp_dic['fnarea']=i[0].fnarea
            temp_dic['jobtype']=i[0].jobtype
            final_vals.append(temp_dic)
        count=len(final_vals)
        GET_params = request.GET.copy()
        if('page' in GET_params):
            last=GET_params['page'][-1]
            GET_params['page']=last[0]
        p=Paginator(final_vals, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
    return render(request, 'jobsuggest-candidate.html', {'pk': pk, 'pe': page_obj, 'count': count})

def logout(request, pk):
    user=Login.objects.get(log_id=JobSeeker.objects.get(user_id=pk).log_id.log_id)
    user.status=0
    user.save()
    request.session.flush()
    return redirect('main:index')
