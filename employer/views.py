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

from main.utils import send_emails

# Create your views here.
def dashboard(request, pk):
    context = Employer.objects.get(eid=pk)
    jobs = Jobs.objects.filter(eid=pk)
    applics = Application.objects.filter(eid=pk)
    visits = ProfileVisits.objects.filter(user_type="e", e_id=pk)
    all_notis = []
    count=0
    recent_candidates=[]
    num_notif = Notifications.objects.filter(rece_id=context.log_id).order_by('-datetime')
    for i in num_notif:
        single_notis={}
        single_notis['notif_type']=i.notif_type
        single_notis['datetime']=i.datetime
        user=JobSeeker.objects.get(log_id=i.send_id)
        single_notis['name']=user.name
        single_notis['user_id']=user.user_id
        single_notis['log_id']=user.log_id.log_id
        heapq.heappush(recent_candidates, (i.datetime, user.user_id, user.photo, user.name, user.title, user.location, user.log_id.log_id))
        # recent_candidates.put([i.datetime, user.user_id, user.photo, user.name, user.title, user.location])
        if i.job_id:
            job=jobs.filter(jobid=i.job_id.jobid)
            single_notis['title']=job[0].title
            single_notis['jobid']=job[0].jobid
        if i.testuser_id:
            testinfo=TestInfo.objects.get(test_id=i.testuser_id.test_id)
            single_notis['test_name']=testinfo.test_name
            single_notis['test_id']=i.testuser_id.testuser_id
        all_notis.append(single_notis)
        count=count+1
        if(count>10):
            break
    threads = Threads.objects.filter(sender=context.log_id)
    countunmess=0
    recent_mess=[]
    # for i in applics:
    #     jobseek=JobSeeker.objects.get(user_id=i.user_id.user_id)
    #     heapq.heappush(recent_candidates, (i.date_applied, jobseek.user_id, jobseek.photo, jobseek.name, jobseek.title, jobseek.location))
    for i in threads:
        mess=Messages.objects.filter(msg_id=i.msg_id, receiver_user=context.log_id.log_id).order_by("-date")
        if(len(mess)>0):
            countunmess=countunmess+len(mess.filter(is_read=0))
            tempval=[]
            tempval.append(mess[0].date)
            tempval.append(mess[0].body)
            jobseek=JobSeeker.objects.get(log_id=mess[0].sender_user.log_id)
            tempval.append(jobseek.name)
            tempval.append(jobseek.photo)
            heapq.heappush(recent_candidates, (mess[0].date, jobseek.user_id, jobseek.photo, jobseek.name, jobseek.title, jobseek.location, jobseek.log_id.log_id))
            # recent_candidates.put([mess[0].date, jobseek.user_id, jobseek.photo, jobseek.name, jobseek.title, jobseek.location])
            recent_mess.append(tempval)
    finalrecent=[]
    count=0
    existing=[]
    while recent_candidates:
        temp=recent_candidates.pop()
        if temp[1] not in existing:
            finalrecent.append(temp)
            count=count+1
            if(count>10):
                break
        existing.append(temp[1])
    recent_mess.sort(reverse=True)
    recent_mess_temp=[]
    idx=min(4, len(recent_mess))
    for i in range(0, idx):
        recent_mess_temp.append(recent_mess[i])
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
    nums=[len(jobs), len(applics), countunmess]
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'dashboard-employer.html', {'pk': pk, 'nums': nums, 'notifics': all_notis, 'recent': recent_mess_temp, 'candi': finalrecent, 'charts': charts_context, 'counts': counts})

def newjob(request, pk):
    if(request.method=="POST"):
        job=Jobs()
        job.eid=Employer.objects.get(eid=pk)
        job.title=request.POST['title']
        job.location=request.POST['location']
        job.fnarea=request.POST['fnarea']
        job.jobdesc=request.POST['description']
        job.experience=request.POST['experience']
        job.careerlevel=request.POST['careerlevel']
        job.jobtype=request.POST['jobtype']
        job.basicpay=request.POST['basicpay']
        job.skills=request.POST['skills']
        job.responsibilities=request.POST['responsibilities']
        job.requirements=request.POST['requirements']
        job.save()
        request.session['c_s_id']=job.jobid
        return redirect('employer:cand_suggest', pk=pk)
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'newjob-employer.html', {'pk': pk})

def edit(request, pk):
    context = Employer.objects.get(eid=pk)
    if request.method=="POST":
        context.ename = request.POST['ename']
        loger  = Login.objects.get(email=request.session['email'])
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
        filev=None
        try:
            filev=request.FILES['logo']
            lst=filev._name.split(".")
            filev._name=str(pk)+"_"+context.ename+"_Photo_"+filev._name
            if context.logo:
                context.logo.delete()
            context.logo = filev
        except:
            filev=None
        filev=None
        try:
            filev=request.FILES['cover']
            lst=filev._name.split(".")
            filev._name=str(pk)+"_"+context.ename+"_Cover_"+filev._name
            if context.cover:
                context.cover.delete()
            context.cover = filev
        except:
            filev=None
        context.save()
        return redirect('employer:cedit', pk=pk)
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'profile-employer.html', {'pk': pk, 'context': context})

def returnvalue(phone):
	return str(phone) + str(datetime.date(datetime.now())) + "12345"

def get_ot(request, pk):
	if request.method == "GET":
		key = base64.b32encode(returnvalue(request.GET['phone']).encode())
		OTP = pyotp.TOTP(key,interval = 30)
		return JsonResponse({'OTP': OTP.now()})
	return JsonResponse({'OTP': 'X'})

def post_ot(request, pk):
	if(request.method=='POST'):
		key = base64.b32encode(returnvalue(request.POST['phone'][3:]).encode())
		OTP = pyotp.TOTP(key,interval = 30)
		if OTP.verify(int(request.POST['OTP'])):
			return JsonResponse({'message': 'Phone number verified'})
	return JsonResponse({'message': 'Please enter correct OTP'})

def cupd_phone(request, pk):
    if request.method=="POST":
        employ=Employer.objects.get(eid=pk)
        employ.phone=request.POST['phone']
        employ.save()
        return JsonResponse({'message': 'x'})

def manage(request, pk):
    if request.method=="POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                Jobs.objects.filter(jobid=i).delete()
            return redirect('employer:manage', pk=pk)
        Jobs.objects.filter(jobid=request.POST['job_id']).delete()
        return redirect('employer:manage', pk=pk)
    all_jobs = Jobs.objects.filter(eid=pk).order_by('-postdate')
    all_det = []
    for i in all_jobs:
        data={}
        data['jobid']=i.jobid
        data['title']=i.title
        data['location']=i.location
        data['fnarea']=i.fnarea
        data['jobtype']=i.jobtype
        applications=Application.objects.filter(job_id=i.jobid)
        data['num']=len(applications)
        data['postdate']=i.postdate
        all_det.append(data)
    count=len(all_jobs)
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
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'managejob-employer.html', {'pk': pk, 'pe': page_obj, 'count': count})

def candidates(request, pk):
    shower=""
    if 'shower' in request.session:
        shower=request.session['shower']
    if request.method=="POST":
        if 'approve' in request.POST:
            apps=Application.objects.get(apply_id=request.POST['apply_id'])
            request.session['shower']=apps.job_id.jobid
            apps.status=1
            apps.save()
            subject="Congratulations "+apps.user_id.name+" you are selected!"
            message="Company: "+apps.job_id.eid.ename+"\nJob: "+apps.job_id.title
            receipt=[apps.user_id.log_id.email]
            send_emails(subject, message, receipt)
            return redirect('employer:candidates', pk=pk)
        if 'reject' in request.POST:
            apps=Application.objects.get(apply_id=request.POST['apply_id'])
            request.session['shower']=apps.job_id.jobid
            apps.status=2
            apps.save()
            return redirect('employer:candidates', pk=pk)
        if 'act' in request.POST:
            if(request.POST['act']=="delall"):
                for i in request.POST.getlist('ids[]'):
                    ap=Application.objects.filter(apply_id=i)
                    request.session['shower']=ap[0].job_id.jobid
                    ap.delete()
            if(request.POST['act']=="appall"):
                for i in request.POST.getlist('ids[]'):
                    apps=Application.objects.get(apply_id=i)
                    apps.status=1
                    apps.save()
                    subject="Congratulations "+apps.user_id.name+" you are selected!"
                    message="Company: "+apps.job_id.eid.ename+"\nJob: "+apps.job_id.title
                    receipt=[apps.user_id.log_id.email]
                    send_emails(subject, message, receipt)
                    request.session['shower']=apps.job_id.jobid
            if(request.POST['act']=="rejall"):
                for i in request.POST.getlist('ids[]'):
                    apps=Application.objects.get(apply_id=i)
                    apps.status=2
                    apps.save()
                    request.session['shower']=apps.job_id.jobid
            return redirect('employer:candidates', pk=pk)
        ap=Application.objects.filter(apply_id=request.POST['apply_id'])
        request.session['shower']=ap[0].job_id.jobid
        ap.delete()
        return redirect('employer:candidates', pk=pk)
    testinfo=TestInfo.objects.filter(eid=pk)
    applics=Application.objects.filter(eid=pk)
    jobs=Jobs.objects.filter(eid=pk).order_by('-postdate')
    app_count=[]
    single_apps=[]
    for i in jobs:
        app_count.append(len(Application.objects.filter(job_id=i.jobid)))
    if(jobs):
        s_apps=Application.objects.filter(job_id=jobs[0].jobid)
        for i in s_apps:
            single_can={}
            user=JobSeeker.objects.get(user_id=i.user_id.user_id)
            single_can['user_id']=user.user_id
            single_can['name']=user.name
            single_can['location']=user.location
            single_can['photo']=user.photo
            job=Jobs.objects.get(jobid=i.job_id.jobid)
            single_can['jobid']=job.jobid
            single_can['title']=job.title
            single_can['status']=i.status
            single_can['date_applied']=i.date_applied
            single_can['apply_id']=i.apply_id
            single_can['log_id']=user.log_id.log_id
            if i.status == 4:
                testinfo1=TestInfo.objects.get(testinfoid=i.test.testinfoid)
                testuser1=TestUser.objects.get(test_id=testinfo1.test_id.test_id, user_id=user.user_id)
                single_can['results']=(int(testuser1.correct_answers)/int(testuser1.total_ques))*100
                print(single_can['results'])
            else:
                single_can['results']=0
            single_apps.append(single_can)
    all_can=[]
    for i in applics:
        single_can={}
        user=JobSeeker.objects.get(user_id=i.user_id.user_id)
        single_can['user_id']=user.user_id
        single_can['name']=user.name
        single_can['location']=user.location
        single_can['photo']=user.photo
        job=Jobs.objects.get(jobid=i.job_id.jobid)
        single_can['jobid']=job.jobid
        single_can['title']=job.title
        single_can['status']=i.status
        single_can['date_applied']=i.date_applied
        single_can['apply_id']=i.apply_id
        single_can['log_id']=user.log_id.log_id
        if i.status == 4:
            testinfo1=TestInfo.objects.get(testinfoid=i.test.testinfoid)
            testuser1=TestUser.objects.get(test_id=testinfo1.test_id.test_id, user_id=user.user_id)
            single_can['results']=(int(testuser1.correct_answers)/int(testuser1.total_ques))*100
        else:
            single_can['results']=0
        all_can.append(single_can)
    count=len(all_can)
    all_can = sorted(all_can, key=lambda d: d['date_applied'])
    all_can.reverse()
    GET_params = request.GET.copy()
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(all_can, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'candidate-employer.html', {'pk': pk, 'pe': page_obj, 'count': count, 'jobs': jobs, 'app_count': app_count, 'single': single_apps, 'shower': shower, 'test': testinfo})

def get_candidate(request, pk):
    candidate = JobSeeker.objects.get(user_id=request.GET['user_id'])
    loger = Login.objects.get(log_id=candidate.log_id.log_id)
    cand={}
    emp=Employer.objects.get(eid=pk)
    if(candidate.photo):
        cand['photo']=candidate.photo.url
    cand['name']=candidate.name
    cand['about']=candidate.about
    cand['email']=loger.email
    cand['location']=candidate.location
    cand['phone']=candidate.phone
    cand['title']=candidate.title
    if(candidate.skills):
        cand['skills']=candidate.skills.split(",")
    work=ExperienceJob.objects.filter(user_id=candidate.user_id)
    edu=Education.objects.filter(user_id=candidate.user_id)
    visit=ProfileVisits()
    visit.e_id=emp
    visit.user_id=candidate
    visit.user_type="c"
    visit.save()
    notif=Notifications()
    notif.notif_type="V"
    notif.send_id=Login.objects.get(email=request.session['email'])
    notif.rece_id=loger
    notif.save()
    return JsonResponse({'info': dumps(cand, default=str), 'work': dumps(list(work.values())), 'edu': dumps(list(edu.values()))})

def subscriptions(request, pk):
    return render(request, 'subscriptions-employer.html', {'pk': pk})

def change_pass(request, pk):
    if request.method=="POST":
        user=Login.objects.get(email=request.session['email'])
        if(check_password(request.POST['old'], user.password)):
            if request.POST['new']!=request.POST['cnew']:
                messages.error(request, "Both your password and your confirmation password must be exactly same")
                return redirect('employer:change_pass', pk=pk)
            if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['new']):
                messages.error(request, "Please entere a valid password")
                return redirect('employer:change_pass', pk=pk)
            if(request.POST['old']==request.POST['new']):
                messages.error(request, "Old and new password cant be same")
                return redirect('employer:change_pass', pk=pk)
            user.password=make_password(request.POST['new'])
            user.save()
            request.session['password']=user.password
            messages.success(request, 'Password changed successfully')
            return redirect('employer:change_pass', pk=pk)
        else:
            messages.error(request, "Please enter correct old password")
            return redirect('employer:change_pass', pk=pk)
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'password-employer.html', {'pk': pk})

def cinbox(request, pk):
    shower=""
    if 'thread' in request.session:
        shower=request.session['thread']
        del request.session['thread']
    loger=Login.objects.get(email=request.session['email'])
    threads=Threads.objects.filter(sender=loger.log_id)
    temp_threads=[dumps(list(threads.values()), default=str)]
    all_threads=[]
    all_messages=[]
    messages=[]
    for i in threads:
        single_thread={}
        mess=Messages.objects.filter(msg_id=i.msg_id).order_by("date")
        messages.append(dumps(list(mess.values()), default=str))
        all_messages.append(mess)
        n=len(mess)
        if(n==0):
            single_thread['date']=i.date
            single_thread['body']=""
            single_thread['end']="x"
        else:
            single_thread['date']=mess[n-1].date
            single_thread['body']=mess[n-1].body
            if(mess[n-1].sender_user.log_id==loger.log_id):
                single_thread['end']="y"
            else:
                single_thread['end']="c"
        single_thread['msg_id']=i.msg_id
        recei=JobSeeker.objects.get(log_id=i.receiver.log_id)
        single_thread['name']=recei.name
        single_thread['photo']=recei.photo
        single_thread['sender']=i.sender
        single_thread['receiver']=i.receiver
        all_threads.append(single_thread)
    all_threads.reverse()
    all_messages.reverse()
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'cinbox-employer.html', {'pk': pk, 'threads': all_threads, 'm': all_messages, 'mess': messages, 'thre': temp_threads, 'shower': shower})


def sendmess(request, pk):
    if(request.method=="POST"):
        thread=Threads.objects.get(msg_id=request.POST['candidate'])
        message=Messages()
        message.msg_id=thread
        message.sender_user=Login.objects.get(email=request.session['email'])
        message.receiver_user=Login.objects.get(log_id=thread.receiver.log_id)
        message.body=request.POST['message']
        message.save()
        user=Login.objects.get(email=request.session['email'])
        threads=Threads.objects.filter(sender=user.log_id)
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
        notif.rece_id=Login.objects.get(log_id=thread.receiver.log_id)
        notif.save()
        return JsonResponse({'message': 'Y', 'id': request.POST['candidate'], 'thre': temp_threads, 'm': messages})


def fetch(request, pk):
    if request.GET['candidate']=="":
        return JsonResponse({'message': 'X'})
    user=Login.objects.get(email=request.session['email'])
    threads=Threads.objects.filter(sender=user.log_id)
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
                username=JobSeeker.objects.get(log_id=mess[n-1].sender_user.log_id)
                rece.append({'msg_id': i.msg_id, 'body': username.name+": "+mess[len(mess)-1].body, 'type': "c"})
        mess_all.append(dumps(list(mess.values()), default=str))
    comp_thread=Threads.objects.get(msg_id=request.GET['candidate'])
    comp_log=Login.objects.get(log_id=comp_thread.receiver.log_id)
    thread=dumps(list(Threads.objects.filter(msg_id=request.GET['candidate']).values()), default=str)
    messa=dumps(list(Messages.objects.filter(msg_id=request.GET['candidate'], receiver_user=user.log_id, is_read=False).values()), default=str)
    company=dumps(list(JobSeeker.objects.filter(log_id=comp_log).values()), default=str)
    urlval=JobSeeker.objects.filter(log_id=comp_log)[0].photo.url
    return JsonResponse({'message': 'Y', 'url': "", 'mess': messages, 'thre': temp_threads, 'count': count, 'thread': thread, 'company': company ,'messa': messa, 'all_mess': mess_all, 'image': urlval, 'unread': dumps(ind_unread), 'rece': dumps(rece)})


def seen(request, pk):
    loger=Login.objects.get(email=request.session['email'])
    if(request.method=="POST"):
        if request.POST['candidate']=="":
            return JsonResponse({'message': 'X'})
        messages=Messages.objects.filter(msg_id=request.POST['candidate'], receiver_user=loger.log_id, is_read=False)
        Messages.objects.filter(msg_id=request.POST['candidate'], receiver_user=loger.log_id, is_read=False).update(is_read=True)
        for i in messages:
            i.is_read=True
            i.save()
        return JsonResponse({'message': 'Y'})

def inbox_count(request, pk):
    # user=JobSeeker.objects.get(user_id=pk)
    # num_mess=Threads.objects.filter(receiver=user.log_id, has_unread=1)
    loger=Login.objects.get(email=request.session['email'])
    countval=len(Messages.objects.filter(receiver_user=loger.log_id, is_read=False))
    return JsonResponse({'count': countval})

def delete_mess(request, pk):
    if request.method == "POST":
        Threads.objects.get(msg_id=request.POST['candidate']).delete()
        return JsonResponse({'message': 'a'})

def createthread(request, pk):
    if request.method=="POST":
        loger=Employer.objects.get(eid=pk)
        msg=Threads.objects.filter(sender=loger.log_id.log_id, receiver=request.POST['receiver'])
        if(len(msg)>0):
            request.session['thread']=msg[0].msg_id
            return JsonResponse({'url': ""})
        else:
            newthread=Threads()
            newthread.sender=loger.log_id
            newthread.receiver=Login.objects.get(log_id=request.POST['receiver'])
            newthread.save()
            request.session['thread']=newthread.msg_id
            return JsonResponse({'url': ""})
    return JsonResponse({'url': ""})

def cnotifications(request, pk):
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
        user = JobSeeker.objects.get(log_id=i.send_id)
        single_notif['user_id']=user.user_id
        single_notif['log_id']=user.log_id
        single_notif['name']=user.name
        if i.job_id:
            jobs = Jobs.objects.get(jobid=i.job_id.jobid)
            single_notif['title']=jobs.title
            single_notif['jobid']=jobs.jobid
        if i.testuser_id:
            testinfo=TestInfo.objects.get(test_id=i.testuser_id.test_id)
            single_notif['test_name']=testinfo.test_name
            single_notif['test_id']=i.testuser_id.testuser_id
        nots.append(single_notif)
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
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'cnotifications-employer.html', {'pk': pk, 'notif': page_obj})

def under_development(request, pk):
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'under_develop.html', {'pk': pk})

def jobapp(request, pk):
    jobinfo = Jobs.objects.filter(jobid=request.GET['jobid'])
    employer = Employer.objects.filter(eid=pk)
    image=""
    if(employer[0].logo):
        image = str(employer[0].logo.url)
    return JsonResponse({'logo': image, 'info': dumps(list(jobinfo.values()), default=str), 'company': dumps(list(employer.values()))})

def edit_job(request, pk):
    job=None
    if(request.method=="GET"):
        job = Jobs.objects.filter(jobid=request.GET['jobid'])
    else:
        job = Jobs.objects.filter(jobid=request.POST['jobid'])
    if request.method=="POST":
        if(len(job)>0):
            job[0].title=request.POST['title']
            job[0].location=request.POST['location']
            job[0].fnarea=request.POST['fnarea']
            job[0].jobdesc=request.POST['description']
            job[0].experience=request.POST['experience']
            job[0].careerlevel=request.POST['careerlevel']
            job[0].jobtype=request.POST['jobtype']
            job[0].basicpay=request.POST['basicpay']
            job[0].skills=request.POST['skills']
            job[0].responsibilities=request.POST['responsibilities']
            job[0].requirements=request.POST['requirements']
            job[0].save()
        return redirect('employer:manage', pk=pk)
    return JsonResponse({'info': dumps(list(job.values()), default=str)})

def cand_suggest(request, pk):
    job = Jobs.objects.filter(eid=pk)
    candid=[]
    sel=""
    if ('job_id' in request.GET and request.GET['job_id']!='a') or 'c_s_id' in request.session:
        single_job=None
        if 'c_s_id' in request.session:
            sel=int(request.session['c_s_id'])
            single_job = Jobs.objects.get(jobid=request.session['c_s_id'])
            del request.session['c_s_id']
        else:
            sel=int(request.GET['job_id'])
            single_job = Jobs.objects.get(jobid=request.GET['job_id'])
        jobs=JobSeeker.objects.all()
        for i in jobs:
            if i.Resume:
                try: 
                    pdfFileObj = open("media/"+str(i.Resume),'rb')  
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                except:
                    continue
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
                    if area.lower() == single_job.title.lower():
                        for word in terms[area]:
                            if word in text:
                                quality +=1
                        break
                single_candidate={}
                single_candidate['user_id']=i.user_id
                single_candidate['name']=i.name
                if i.photo:
                    single_candidate['photo']=i.photo
                single_candidate['score']=quality
                single_candidate['location']=i.location
                candid.append(single_candidate)
    GET_params = request.GET.copy()
    count=len(candid)
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(candid, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    if 'shower' in request.session:
        del request.session['shower']
    return render(request, 'suggestions-employer.html', {'pk': pk, 'jobs': job, 'count': count, 'pe': page_obj, 'sel': sel})

def get_cands(request, pk):
    applics=Application.objects.filter(job_id=request.GET['jobid'])
    single_apps=[]
    for i in applics:
        single_can={}
        user=JobSeeker.objects.get(user_id=i.user_id.user_id)
        single_can['user_id']=user.user_id
        single_can['name']=user.name
        single_can['location']=user.location
        single_can['photo']=user.photo.url
        job=Jobs.objects.get(jobid=i.job_id.jobid)
        single_can['jobid']=job.jobid
        single_can['title']=job.title
        single_can['status']=i.status
        if i.status == 4:
            testinfo1=TestInfo.objects.get(testinfoid=i.test.testinfoid)
            testuser1=TestUser.objects.get(test_id=testinfo1.test_id.test_id, user_id=user.user_id)
            single_can['results']=(int(testuser1.correct_answers)/int(testuser1.total_ques))*100
        else:
            single_can['results']=0
        single_can['date_applied']=i.date_applied
        single_can['apply_id']=i.apply_id
        single_can['log_id']=user.log_id.log_id
        single_apps.append(single_can)
    return JsonResponse({'info': dumps(single_apps, default=str)})

def quiz(request, pk):
    quizzes = Quiz.objects.filter(eid=pk)
    quiz = []
    for i in quizzes:
        single_quiz={}
        single_quiz['quiz_id']=i.quiz_id
        single_quiz['created_date']=i.created_date
        single_quiz['time_limit']=i.time_limit
        job=Jobs.objects.get(jobid=i.job_id.jobid)
        single_quiz['jobid']=job.jobid
        single_quiz['location']=job.location
        single_quiz['title']=job.title
        single_quiz['fnarea']=job.fnarea
        single_quiz['jobtype']=job.jobtype
        quiz.append(single_quiz)
    GET_params = request.GET.copy()
    count=len(quiz)
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(quiz, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'quiz-employer.html', {'pk': pk, 'count': count, 'pe': page_obj})

def show_tests(request, pk):
    if request.method=="POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                Test.objects.get(test_id=i).delete()
            return redirect('employer:show_tests', pk=pk)
        Test.objects.get(test_id=request.POST['test_id']).delete()
        return redirect('employer:show_tests', pk=pk)
    tests=TestInfo.objects.filter(eid=pk)
    all_tests = []
    for i in tests:
        single_test={}
        single_test['test_id']=i.test_id.test_id
        single_test['testinfoid']=i.testinfoid
        single_test['created_date']=i.test_id.created_date
        single_test['time_limit']=i.time_limit
        single_test['name']=i.test_name
        questions=TestQues.objects.filter(testinfoid=i.testinfoid)
        single_test['num']=len(questions)
        all_tests.append(single_test)
    sorted(all_tests, key=lambda i: i['created_date'])
    all_tests.reverse()
    GET_params = request.GET.copy()
    count=len(all_tests)
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(all_tests, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'show-employer.html', {'pk': pk, 'pe': page_obj, 'count': count})

def create_test(request, pk):
    if request.method=="POST":
        test=Test()
        test.save()
        testinfo=TestInfo()
        testinfo.test_id=test
        testinfo.test_name=request.POST['name']
        testinfo.eid=Employer.objects.get(eid=pk)
        testinfo.time_limit=request.POST['timelimit']
        testinfo.save()
        info=request.POST.getlist('desc')
        options=request.POST.getlist('optdesc')
        correct=request.POST.getlist('correct')
        n=len(info)
        count=0
        for i in range(0, n):
            single=TestQues()
            single.testinfoid=testinfo
            single.ques_name=info[i]
            single.option1=options[count]
            single.option2=options[count+1]
            single.option3=options[count+2]
            single.option4=options[count+3]
            count=count+4
            single.correct=correct[i]
            single.save()
        return redirect('employer:test', pk=pk)
    return render(request, 'create_quiz-employer.html', {'pk':pk})

def schedule(request, pk):
    if request.method=="POST":
        if 'ids[]' in request.POST:
            ids=request.POST.getlist('ids[]')
            f=False
            for i in ids:
                flag=False
                applics=Application.objects.get(apply_id=i)
                if applics.status==3:
                    flag=True
                    f=True
                if(flag==False):
                    testinfo=TestInfo.objects.get(testinfoid=request.POST['testinfoid'])
                    tuser=TestUser.objects.filter(user_id=applics.user_id, test_id=testinfo.test_id.test_id)
                    if(len(tuser)>0):
                        break
                    applics.status=3
                    request.session['shower']=applics.job_id.jobid
                    testuser=TestUser()
                    testuser.user_id=applics.user_id
                    testuser.test_id=testinfo.test_id
                    applics.test=testinfo
                    applics.save()
                    testuser.save()
                    notif=Notifications()
                    notif.notif_type="T"
                    notif.send_id=Login.objects.get(email=request.session['email'])
                    notif.rece_id=applics.user_id.log_id
                    notif.save()
                    subject="Test scheduled by "+applics.job_id.eid.ename
                    message="Test Name: "+testinfo.test_name+"\nDuration: "+str(testinfo.time_limit)
                    receipt=[applics.user_id.log_id.email]
                    send_emails(subject, message, receipt)
            return JsonResponse({'message': 'scheduled'})
        applics=Application.objects.get(apply_id=request.POST['id'])
        if applics.status==3:
            return JsonResponse({'message': 'X'})
        testinfo=TestInfo.objects.get(testinfoid=request.POST['testinfoid'])
        tuser=TestUser.objects.filter(user_id=applics.user_id, test_id=testinfo.test_id.test_id)
        if(len(tuser)>0):
            return JsonResponse({'message': 'X'})
        applics.status=3
        request.session['shower']=applics.job_id.jobid
        testuser=TestUser()
        testuser.user_id=applics.user_id
        testuser.test_id=testinfo.test_id
        applics.test=testinfo
        applics.save()
        testuser.save()
        notif=Notifications()
        notif.notif_type="T"
        notif.send_id=Login.objects.get(email=request.session['email'])
        notif.rece_id=applics.user_id.log_id
        notif.save()
        subject="Test scheduled by "+applics.job_id.eid.ename
        message="Test Name: "+testinfo.test_name+"\nDuration: "+str(testinfo.time_limit)
        receipt=[applics.user_id.log_id.email]
        send_emails(subject, message, receipt)
    return JsonResponse({'message': 'scheduled'})

def test_info(request, pk):
    testinfo=TestInfo.objects.filter(testinfoid=request.GET['testinfoid'])
    testdate=str(testinfo[0].test_id.created_date)
    testquest=TestQues.objects.filter(testinfoid=testinfo[0].testinfoid)
    testdate=testdate[0:11]
    return JsonResponse({'message': 'x', 'test': dumps(list(testinfo.values()), default=str), 'date': dumps(testdate, default=str), 'ques': dumps(list(testquest.values()))})

def get_results(request, pk):
    testuser=TestUser.objects.get(testuser_id=request.GET['id'])
    testinfo=TestInfo.objects.get(test_id=testuser.test_id.test_id)
    data={}
    data['user_id']=testuser.user_id.user_id
    inters=Interview.objects.filter(user_id=testuser.user_id.user_id, eid=pk)
    data['user_name']=testuser.user_id.name
    data['name']=testinfo.test_name
    data['num']=testuser.total_ques
    data['correct']=testuser.correct_answers
    data['date']=testuser.date
    if(len(inters)>0):
        data['int_link']=inters[0].int_link
    else:
        data['int_link']=""
    data['percent']=(data['correct']/data['num'])*100
    return JsonResponse({'data': dumps(data, default=str)})

def schedule_interview(request, pk):
    if request.method=="POST":
        check=Interview.objects.filter(user_id=request.POST['user_id'], eid=pk)
        if(len(check)!=0):
            check[0].int_link=request.POST['int_link']
            check[0].save()
            return JsonResponse({'m': 'A'})
        intval=Interview()
        intval.eid=Employer.objects.get(eid=pk)
        intval.user_id=JobSeeker.objects.get(user_id=request.POST['user_id'])
        intval.int_link=request.POST['int_link']
        intval.is_done=False
        intval.is_feedgiven=False
        intval.save()
        notif=Notifications()
        notif.notif_type="I"
        notif.send_id=intval.eid.log_id
        notif.rece_id=intval.user_id.log_id
        notif.save()
        subject="Interview scheduled by "+intval.eid.ename
        message="Interview link: "+intval.int_link+"\nDate: "+str(intval.schedule_date)
        receipt=[intval.user_id.log_id.email]
        send_emails(subject, message, receipt)
        return JsonResponse({'m': 'Y'})
    return JsonResponse({'m': 'X'})

def all_interviews(request, pk):
    if request.method=="POST":
        if 'act' in request.POST:
            if request.POST['act']=="donall":
                for i in request.POST.getlist('ids[]'):
                    single_int=Interview.objects.get(int_id=i)
                    single_int.is_done=1
                    single_int.save()
                return redirect('employer:all_interviews', pk=pk)
            for i in request.POST.getlist('ids[]'):
                Interview.objects.get(int_id=i).delete()
            return redirect('employer:all_interviews', pk=pk)
        Interview.objects.get(int_id=request.POST['int_id']).delete()
        return redirect('employer:all_interviews', pk=pk)
    all_ints=Interview.objects.filter(eid=pk).order_by('-schedule_date')
    final_ints=[]
    for i in all_ints:
        single_int={}
        single_int['int_id']=i.int_id
        single_int['user_id']=i.user_id.user_id
        single_int['name']=i.user_id.name
        single_int['location']=i.user_id.location
        single_int['date']=i.schedule_date
        single_int['link']=i.int_link
        single_int['isdone']=i.is_done
        final_ints.append(single_int)
    GET_params = request.GET.copy()
    count=len(final_ints)
    if('page' in GET_params):
        last=GET_params['page'][-1]
        GET_params['page']=last[0]
    p=Paginator(final_ints, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'interviews-employer.html', {'pk': pk, 'pe': page_obj, 'count': count})

def done(request, pk):
    if request.method=="POST":
        int_val = Interview.objects.get(int_id=request.POST['id'])
        int_val.is_done=1
        int_val.save()
        return JsonResponse({'message': 'Y'})

def get_link(request, pk):
    int_val=Interview.objects.get(int_id=request.GET['int_id'])
    name=int_val.user_id.name
    if int_val.is_done==0:
        return JsonResponse({'message': 'X', 'name': name})
    url="http://localhost:8000/give_feedback/"+str(int_val.int_id)+"/"
    data=[]
    if int_val.cand_feedback:
        data.append(int_val.cand_feedback)
    else:
        data.append(False)
    all_feeds=Feedback.objects.filter(int_id=request.GET['int_id'])
    if all_feeds:
        for i in all_feeds:
            data.append([i.name, i.emp_feedback])
    else:
        data.append(False)
    return JsonResponse({'message': 'Y', 'url': url, 'name': name, 'info': data})

def logout(request, pk):
    employer=Login.objects.get(log_id=Employer.objects.get(eid=pk).log_id.log_id)
    employer.status=0
    employer.save()
    request.session.flush()
    return redirect('main:index')







