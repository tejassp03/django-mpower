from django.shortcuts import render
from main.models import JobSeeker, Employer, Jobs, Application, Selection, Login
from json import dumps
# Create your views here.
def dashboard(request, pk):
    # print(request.session['email'])
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
    context = JobSeeker.objects.get(user_id=pk)
    email = Login(context.log_id)
    skills=context.skills.split(",")
    for i in skills:
        if i=="":
            skills.remove(i)
    experiences=context.experience.split(",")
    for i in range(0, len(experiences)):
        if experiences[i]=="":
            experiences.remove(experiences[i])
        else:
            experiences[i]=experiences[i].split(",")
    return render(request, 'profile-candidate.html', {'user': context, 'pk': pk, 'log': email, 'skills': skills, 'experiences': experiences})