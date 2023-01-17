from django.shortcuts import render, redirect
from main.models import JobSeeker, Employer, Jobs, Application, Selection, Login, ExperienceJob, Education
from json import dumps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.
def dashboard(request, pk):
    context = JobSeeker.objects.get(user_id=pk)
    applics = list(Application.objects.filter(user_id=pk).values())
    fordates = Application.objects.filter(user_id=pk).order_by('-date_applied')
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
    return render(request, 'dashboard-candidate.html', {'user': context, 'applications': applics, 'pk': pk})


def edit_profile(request, pk):
    if(request.method=="DELETE"):
        print("cehck")
    if(request.method=="POST" and request.POST['skill']):
        user = JobSeeker.objects.get(user_id=pk)
        if(user.skills):
            user.skills=user.skills+","+request.POST['skill']
        else:
            user.skills=request.POST['skill']
        user.save()
    if(request.method=="POST" and (request.POST['job_title'] or request.POST['company'] or request.POST['time_period'] or request.POST['description'])):
        exper = ExperienceJob()
        user=JobSeeker.objects.get(user_id=pk)
        exper.user_id=user
        exper.job_title=request.POST['job_title']
        exper.company=request.POST['company']
        exper.time_period=request.POST['time_period']
        exper.description=request.POST['description']
        exper.save()
    if(request.method=="POST" and (request.POST['title'] or request.POST['school'] or request.POST['period_edu'] or request.POST['desc'])):
        edu = Education()
        user=JobSeeker.objects.get(user_id=pk)
        edu.user_id=user
        edu.title=request.POST['title']
        edu.school=request.POST['school']
        edu.time_period=request.POST['period_edu']
        edu.description=request.POST['desc']
        edu.save()
    if(request.method=="POST" and (request.POST['name'] or request.POST['title'] or request.POST['location'] or request.POST['email'] or request.POST['phone'] or request.POST['about'] or request.FILES)):
        jobseeker=JobSeeker.objects.get(user_id=pk)
        jobseeker.name=request.POST['name']
        jobseeker.title=request.POST.getlist('title')[0]
        jobseeker.location=request.POST['location']
        jobseeker.phone=request.POST['phone']
        jobseeker.about=request.POST['about']
        filev=None
        try:
            filev=request.FILES['photo']
            lst=filev._name.split(".")
            filev._name=str(pk)+"_"+jobseeker.name+"_Photo_"+filev._name
            jobseeker.photo = filev
        except:
            filev=None
        finder=Login.objects.get(email=request.session['email'])
        finder.email=request.POST['email']
        finder.save()
        jobseeker.save()
        request.session['email']=request.POST['email']
    context = JobSeeker.objects.get(user_id=pk)
    skills = context.skills.split(",")
    experience = ExperienceJob.objects.filter(user_id=pk)
    education = Education.objects.filter(user_id=pk)
    for i in skills:
        if i=="":
            skills.remove(i)
    return render(request, 'profile-candidate.html', {'user': context, 'pk': pk, 'log': request.session['email'], 'skills': skills, 'experience': experience, 'education': education})


def add_exp(request, pk):
    if(request.method=="POST"):
        edu = ExperienceJob()
        user=JobSeeker.objects.get(user_id=pk)
        edu.user_id=user
        edu.title=request.POST['title']
        edu.school=request.POST['school']
        edu.time_period=request.POST['period_edu']
        edu.description=request.POST['desc']
        edu.save()
    return redirect('candidate:edit', pk=pk)

# @csrf_exempt
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


# @csrf_exempt
def delete_exp(request, pk):
    if request.method == "POST":
        exp = ExperienceJob.objects.get(exp_id=request.POST['id'])
        exp.delete()
    return redirect('candidate:edit', pk=pk)

# @csrf_exempt
def delete_edu(request, pk):
    if request.method == "POST":
        edu = Education.objects.get(edu_id=request.POST['id'])
        edu.delete()
    return redirect('candidate:edit', pk=pk)


# def add_skill(request, pk):
#     context = JobSeeker.objects.get(user_id=pk)
#     skills = context.skills.split(",")
#     experience = ExperienceJob.objects.filter(user_id=pk)
#     for i in skills:
#         if i=="":
#             skills.remove(i)
#     if(request.method=="POST"):
#         print("aaya")
#         user = JobSeeker.objects.get(user_id=pk)
#         if(user.skills):
#             user.skills=user.skills+","+request.POST['skill']
#         else:
#             user.skills=request.POST['skill']
#         user.save()
#     return redirect('candidate:edit', user=context, pk=pk, log=request.session['email'], skills=skills, experiece=experience)
