from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import JobSeeker, Login, Employer
import random
import re

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def index(request):
	if request.method == 'POST':
		if request.POST['user'] == 'candidate':
			user=Login.objects.filter(email=request.POST['c_email'])
			if(len(user)==0):
				messages.error(request, "Invalid credentials")
				return render(request, 'index.html')
			else:
				if(user[0].password == request.POST['c_pass']):
					return redirect("candidate:dashboard", pk=user[0].log_id)
				else:
					messages.error(request, "Invalid credentials")
		else:
			print("employer")
	return render(request, 'index.html')

def view_function(request):
    messages.add_message(request, messages.INFO, 'This is an info message')
    messages.add_message(request, messages.ERROR, 'This is an error message')
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

def register(request):
	if request.method=='POST':
		if request.POST['name']=="" or request.POST['email']=="" or request.POST['password']=="" or request.POST['conpass']=="":
			messages.error(request, "Dont forget to fill out every field with the appropriate information")
			return redirect('main:index')
		if(request.POST['password']!=request.POST['conpass']):
			messages.error(request, "Both your password and your confirmation password must be exactly same")
			return redirect('main:index')
		if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['password']):
			messages.error(request, "Please entere a valid password")
			return redirect('main:index')
		user=Login()
		user.email = request.POST['email']
		user.password = request.POST['password']
		user.user_type = request.POST['user']
		user.save()
		if(request.POST['user']=="candidate"):
			jobseeker = JobSeeker()
			rand_num = random.randint(0, 1000000000)
			jobseeker.user_id = rand_num
			jobseeker.log_id = user
			jobseeker.name = request.POST['name']
			jobseeker.save()
			messages.success(request, 'Successfully Registered')
			return redirect('main:profilecompletion', pk=user.log_id)
		elif(request.POST['user']=="employer"):
			employer=Employer()
			rand_num = random.randint(0, 1000000000)
			employer.eid = rand_num
			employer.log_id = user
			employer.ename = request.POST['name']
			employer.save()
			messages.success(request, 'Successfully Registered')
			return redirect('main:eprofile', pk=user.log_id)
	return render(request, 'sign-up.html')

def blog(request):
	return render(request, 'blog-list-1.html')

def companies(request):
	return render(request, 'companies-list-3.html')

def candidates(request):
	return render(request, 'candidates-list-3.html')

def postjob(request):
	return render(request, 'company-dashboard-new-job.html')

def findjobs(request):
	context = {
    'var': 6
    }
	return render(request, 'jobs-list-3.html',context)

def profile_completion(request, pk):
	if request.method=='POST':
		jobseeker=JobSeeker.objects.get(log_id=pk)
		jobseeker.phone=request.POST['code']+request.POST['mobile']
		jobseeker.location=request.POST['address']
		jobseeker.dob=request.POST['dob']
		jobseeker.basic_edu=request.POST['basic']
		jobseeker.master_edu=request.POST['master']
		jobseeker.other_qual=request.POST['other']
		skills = request.POST.getlist('skill')
		all_skills=""
		if(len(skills)==1):
			all_skills=skills[0]
		elif(len(skills)>1):
			for i in range(0, len(skills)):
				if i==len(skills)-1:
					if(skills[i]!=""):
						all_skills=all_skills+","+skills[i]
					break
				if(skills[i]!=""):
					all_skills=all_skills+skills[i]
		experiences = request.POST.getlist('experience')
		all_experiences=""
		if(len(experiences)==1):
			all_experiences=experiences[0]
		elif(len(experiences)>1):
			for i in range(0, len(experiences)):
				if i==len(experiences)-1:
					if(experiences[i]!=""):
						all_experiences=all_experiences+"."+experiences[i]
					break
				if(experiences[i]!=""):
					all_experiences=all_experiences+experiences[i]
		jobseeker.skills=all_skills
		jobseeker.experience=all_experiences
		filev=None
		try:
			filev=request.FILES['resume']
			lst=filev._name.split(".")
			filev._name=str(pk)+"_"+jobseeker.name+"_Resume_"+filev._name
			jobseeker.Resume = filev
		except:
			filev=None
		try:
			filev = request.FILES['photo']
			lst=filev._name.split(".")
			filev._name=str(pk)+"_"+jobseeker.name+"_Photo_"+filev._name
			jobseeker.photo = filev
		except:
			filev=None
		jobseeker.save()
	return render(request, 'profile_completion.html')


def emp_completion(request, pk):
	if request.method=="POST":
		employer=Employer.objects.get(log_id=pk)
		employer.phone=request.POST['code']+request.POST['mobile']
		employer.etype=request.POST['etype']
		employer.industry=request.POST['industry']
		employer.executive=request.POST['executive']
		filev=None
		try:
			filev = request.FILES['logo']
			lst=filev._name.split(".")
			filev._name=str(pk)+"_"+employer.ename+"_Logo_"+filev._name
			employer.logo = filev
		except:
			filev=None
		employer.address=request.POST['address']
		employer.pincode=request.POST['pincode']
		employer.location=request.POST['location']
		employer.profile=request.POST['profile']
		employer.save()
	return render(request, 'emp_completion.html')


def returnvalue(phone):
	return str(phone) + str(datetime.date(datetime.now())) + "12345"

def get_otp(request):
	if request.method == "GET":
		key = base64.b32encode(returnvalue(request.GET['phone']).encode())
		OTP = pyotp.TOTP(key,interval = 30)
		return JsonResponse({'OTP': OTP.now()})
	return JsonResponse({'OTP': 'X'})

@csrf_exempt
def verify_otp(request):
	if(request.method=='POST'):
		key = base64.b32encode(returnvalue(request.POST['phone']).encode())
		OTP = pyotp.TOTP(key,interval = 30)
		if OTP.verify(int(request.POST['OTP'])):
			return JsonResponse({'message': 'Phone number verified'})
	return JsonResponse({'message': 'Please enter correct OTP'})

