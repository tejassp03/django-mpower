from django.shortcuts import render, redirect
from main.models import *

# Create your views here.
def dashboard(request, pk):
    return render(request, 'dashboard-employer.html', {'pk': pk})

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
        job.basicpay=1000
        job.save()
        return redirect('employer:newjob', pk=pk)
    return render(request, 'newjob-employer.html', {'pk': pk})


def under_development(request, pk):
    return render(request, 'under_develop.html', {'pk': pk})
