from django.shortcuts import render, redirect
from main.models import JobSeeker, Employer, Jobs, Application, Selection, Login, ExperienceJob, Education, ProfileVisits, Threads, Messages, ResumeAnalysis
from json import dumps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.
def dashboard(request, pk):
    context = JobSeeker.objects.get(user_id=pk)
    applics = list(Application.objects.filter(user_id=pk).values())
    profile = list(ProfileVisits.objects.filter(user_id=pk))
    fordates = Application.objects.filter(user_id=pk).order_by('-date_applied')
    userobj=JobSeeker.objects.get(user_id=pk)
    num_mess=Threads.objects.filter(receiver=userobj.log_id, has_unread=True)
    for i in applics:
        emplo = list(Employer.objects.filter(eid=i.emp_id).values())
        jobo = list(Jobs.objects.filter(jobid=i.job_id).values())
        i['post']=jobo[0].title
        i['com_name']=emplo[0].ename
        i['industry']=emplo[0].industry
        i['location']=jobo[0].location
        i['logo']=emplo[0].logo
    # i = {'post': 'ABC', 'com_name': 'Microsoft', 'industry': 'software', 'location': 'US'}
    # applics.append(i)
    return render(request, 'dashboard-candidate.html', {'user': context, 'applications': applics, 'pk': pk, 'profile': profile, 'count': len(num_mess)})


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

def logout(request, pk):
    request.session.flush()
    return redirect('main:index')
