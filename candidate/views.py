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


# Create your views here.
def dashboard(request, pk):
    context = JobSeeker.objects.get(user_id=pk)
    applics = Application.objects.filter(user_id=pk)
    profile = list(ProfileVisits.objects.filter(user_id=pk))
    fordates = Application.objects.filter(user_id=pk).order_by('-date_applied')
    userobj=JobSeeker.objects.get(user_id=pk)
    num_mess=Threads.objects.filter(receiver=userobj.log_id, has_unread=True)
    num_notif=Notifications.objects.filter(rece_id=context.log_id).order_by('-datetime')
    all_notis=[]
    threadval=Threads.objects.filter(receiver=userobj.log_id, has_unread=1)
    countunmess=0
    for i in threadval:
        countunmess=countunmess+len(Messages.objects.filter(msg_id=i.msg_id, is_read=0))
    print(countunmess)
    count=0
    for i in num_notif:
        single_notis={}
        single_notis['notif_type']=i.notif_type
        single_notis['datetime']=i.datetime
        emp=Employer.objects.get(log_id=i.send_id)
        single_notis['ename']=emp.ename
        single_notis['eid']=emp.eid
        all_notis.append(single_notis)
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
    graph_val=[]
    dates=[]
    for i in range(0, 7):
        d=date.today()-timedelta(days=i)
        temp = applics.filter(date_applied__year=d.year, date_applied__month=d.month, date_applied__day=d.day)
        graph_val.append(len(temp))
        dates.append(d)
        # appsl=Application.objects.filter(date_applied__gte=d)
    graph_val30=[]
    dates30=[]
    mapin={}
    for i in range(0, 30):
        d=date.today()-timedelta(days=i)
        temp = len(applics.filter(date_applied__year=d.year, date_applied__month=d.month, date_applied__day=d.day))
        graph_val30.append(temp)
        if temp in mapin.keys():
            mapin[temp].append(d)
        else:
            mapin[temp]=[d]
    graph_val30.sort(reverse=True)
    final30=[]
    datefinal30=[]
    finaldic={}
    for i in graph_val30:
        if(len(final30)>=7):
            break
        for j in mapin[i]:
            if(len(datefinal30)>=7):
                break
            if j not in datefinal30:
                final30.append(i)
                datefinal30.append(j)
                finaldic[j]=i
    datefinal30.sort()
    pas30=[]
    pasdat30=[]
    for i in datefinal30:
        pas30.append(finaldic[i])
        pasdat30.append(i)
    charts_context={}
    charts_context['pastthi']=dumps(pas30)
    charts_context['dates30']=dumps(pasdat30, default=str)
    return render(request, 'dashboard-candidate.html', {'user': context, 'applications': all_applics, 'pk': pk, 'profile': profile, 'count': len(num_mess), 'notifics': all_notis, 'messcount': countunmess, 'pastsev': dumps(graph_val), 'dates': dumps(dates, default=str), 'charts': charts_context})


def jobapp(request, pk):
    jobinfo = Jobs.objects.filter(jobid=request.GET['jobid'])
    employer = Employer.objects.filter(eid=jobinfo[0].eid.eid)
    image=""
    if(employer[0].logo):
        image = str(employer[0].logo.url)
    return JsonResponse({'logo': image, 'info': dumps(list(jobinfo.values()), default=str), 'company': dumps(list(employer.values()))})


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
        jobseeker.phone=request.POST['phone']
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


def inbox(request, pk):
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
    for i in threads:
        mess=Messages.objects.filter(msg_id=i.msg_id)
        messages.append(dumps(list(mess.values()), default=str))
        temp_messages.append(mess)
        logs_info=Employer.objects.get(log_id=i.sender.log_id)
        logs_info2=Employer.objects.filter(log_id=i.sender.log_id)
        temp_empls.append(logs_info)
        empls.append(dumps(list(logs_info2.values()), default=str))
    if(temp_empls):
        first=temp_empls[0]
    return render(request, 'inbox-candidate.html', {'pk': pk, 'threads': threads, 'first': first ,'mess': messages, 'thre': temp_threads, 'm': temp_messages, 'emp': empls, 'initial': zip(threads, temp_empls)})


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
    for i in threads:
        mess=Messages.objects.filter(msg_id=i.msg_id, is_read=False)
        count=len(mess)+count
        messages.append(dumps(list(mess.values()), default=str))
        temp_messages.append(mess)
        mess=Messages.objects.filter(msg_id=i.msg_id)
        mess_all.append(dumps(list(mess.values()), default=str))
    comp_thread=Threads.objects.get(msg_id=request.GET['employer'])
    comp_log=Login.objects.get(log_id=comp_thread.sender.log_id)
    thread=dumps(list(Threads.objects.filter(msg_id=request.GET['employer']).values()), default=str)
    messa=dumps(list(Messages.objects.filter(msg_id=request.GET['employer'], is_read=False).values()), default=str)
    company=dumps(list(Employer.objects.filter(log_id=comp_log).values()), default=str)
    urlval=Employer.objects.filter(log_id=comp_log)[0].logo.url
    return JsonResponse({'message': 'Y', 'url': "", 'mess': messages, 'thre': temp_threads, 'count': count, 'thread': thread, 'company': company ,'messa': messa, 'all_mess': mess_all, 'image': urlval})

def seenmes(request, pk):
    if(request.method=="POST"):
        if request.POST['employer']=="":
            return JsonResponse({'message': 'X'})
        messages=Messages.objects.filter(msg_id=request.POST['employer'], is_read=False)
        Messages.objects.filter(msg_id=request.POST['employer'], is_read=False).update(is_read=True)
        for i in messages:
            i.is_read=True
            i.save()
        return JsonResponse({'message': 'Y'})


def resume(request, pk):
    data={}
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
    return render(request, 'resume.html', {'pk': pk, 'context': data})

def count_inbox(request, pk):
    user=JobSeeker.objects.get(user_id=pk)
    num_mess=Threads.objects.filter(receiver=user.log_id, has_unread=1)
    return JsonResponse({'count': len(num_mess)})


def change(request, pk):
    if request.method=="POST":
        user=Login.objects.get(email=request.session['email'])
        if(check_password(request.POST['old'], user.password)):
            if request.POST['new']!=request.POST['cnew']:
                messages.error(request, "Both your password and your confirmation password must be exactly same")
                return redirect('candidate:change', pk=pk)
            if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['new']):
                messages.error(request, "Please entere a valid password")
                return redirect('candidate:change', pk=pk)
            if(request.POST['old']==request.POST['new']):
                messages.error(request, "Old and new password cant be same")
                return redirect('candidate:change', pk=pk)
            user.password=make_password(request.POST['new'])
            user.save()
            request.session['password']=user.password
            print(request.session['password'])
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
    return render(request, 'notification-candidate.html', {'pk': pk, 'notif': page_obj})


def applications(request, pk):
    if request.method=="POST":
        if 'act' in request.POST:
            for i in request.POST.getlist('ids[]'):
                Application.objects.filter(apply_id=i).delete()
            return redirect('candidate:applications', pk=pk)
        Application.objects.filter(apply_id=request.POST['apply_id']).delete()
        return redirect('candidate:applications', pk=pk)
    applics=Application.objects.filter(user_id=pk).order_by("-date_applied")
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
    return render(request, 'applications-candidate.html', {'pk': pk, 'all_app': page_obj, 'GET_params': GET_params})


def logout(request, pk):
    request.session.flush()
    return redirect('main:index')
