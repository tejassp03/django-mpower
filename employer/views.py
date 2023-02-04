from django.shortcuts import render, redirect
from main.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import re

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

def edit(request, pk):
    context = Employer.objects.get(eid=pk)
    if request.method=="POST":
        context.ename = request.POST['ename']
        loger  = Login.objects.get(email=request.session['email'])
        loger.email = request.POST['email']
        request.session['name'] = request.POST['ename']
        request.session['email'] = request.POST['email']
        context.phone = request.POST['phone']
        # context.website = request.POST['website']
        context.profile = request.POST['profile']
        context.industry = request.POST['industry']
        # context.yearfounded = request.POST['yearfounded']
        # context.size = request.POST['size']
        context.location = request.POST['location']
        # context.city = request.POST['city']
        context.address = request.POST['address']
        # context.fblink = request.POST['fblink']
        # context.twlink = request.POST['twlink']
        # context.inlink = request.POST['inlink']
        # context.lnlink = request.POST['lnlink']
        # filev=None
        # try:
        #     filev=request.FILES['logo']
        #     lst=filev._name.split(".")
        #     filev._name=str(pk)+"_"+context.ename+"_Photo_"+filev._name
        #     if context.logo:
        #         context.logo.delete()
        #     context.logo = filev
        # except:
        #     filev=None
        context.save()
    return render(request, 'profile-employer.html', {'pk': pk, 'context': context})

def manage(request, pk):
    return render(request, 'managejob-employer.html', {'pk': pk})

def candidates(request, pk):
    return render(request, 'candidates-employer.html', {'pk': pk})

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
            print(request.session['password'])
            messages.success(request, 'Password changed successfully')
            return redirect('employer:change_pass', pk=pk)
        else:
            messages.error(request, "Please enter correct old password")
            return redirect('employer:change_pass', pk=pk)
    return render(request, 'password-employer.html', {'pk': pk})

def cinbox(request, pk):
    return render(request, 'cinbox-employer.html', {'pk': pk})

def cnotifications(request, pk):
    return render(request, 'cnotifications-employer.html', {'pk': pk})

def under_development(request, pk):
    return render(request, 'under_develop.html', {'pk': pk})

def logout(request, pk):
    employer=Login.objects.get(log_id=Employer.objects.get(eid=pk).log_id.log_id)
    employer.status=0
    employer.save()
    request.session.flush()
    return redirect('main:index')
