from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import JobSeeker, Login, Employer
import random
import re
from django.contrib.auth.hashers import make_password, check_password

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def index(request):
	if request.method == 'POST':
		user=Login.objects.filter(email=request.POST['c_email'])
		if(len(user)==0):
			return JsonResponse({'message': 'X'})
		else:
			if(check_password(request.POST['c_pass'], user[0].password)):
				if(request.POST['user'] == 'candidate'):
					jobseeker=JobSeeker.objects.get(log_id=user[0].log_id)
					if((jobseeker.phone==None or jobseeker.phone=="" or len(jobseeker.phone)<=4) and (jobseeker.location==None or jobseeker.location=="") and (jobseeker.experience==None or jobseeker.experience=="") and (jobseeker.skills==None or jobseeker.skills=="") and (jobseeker.basic_edu==None or jobseeker.basic_edu=="") and (jobseeker.master_edu==None or jobseeker.master_edu=="") and (jobseeker.other_qual==None or jobseeker.other_qual=="") and (jobseeker.dob==None or jobseeker.dob=="") and (jobseeker.Resume=="" or jobseeker.Resume==None) and (jobseeker.photo=="" or jobseeker.photo==None)):
						urlval="profile_completion/"+str(user[0].log_id)
						return JsonResponse({'message': 'Y', 'url': urlval})
					# return redirect('main:profilecompletion', pk=user[0].log_id)
				elif(request.POST['user'] == 'employer'):
					employer=Employer.objects.get(log_id=user[0].log_id)
					if((employer.etype==None or employer.etype=="") and (employer.industry==None or employer.industry=="") and (employer.address==None or employer.address=="") and (employer.pincode==None or employer.pincode=="") and (employer.executive==None or employer.executive=="") and (employer.phone==None or employer.phone=="" or len(employer.phone)<=4) and (employer.location==None or employer.location=="") and (employer.profile==None or employer.profile=="") and (employer.logo=="" or employer.logo==None)):
						urlval="emp_completion/"+str(user[0].log_id)
						return JsonResponse({'message': 'Y', 'url': urlval})
				request.session['email'] = request.POST['c_email']
				request.session['password'] = request.POST['c_pass']
				empls=JobSeeker.objects.get(log_id=user[0].log_id)
				request.session['name']=empls.name
				if(request.POST['user'] == 'candidate'):
					urlval="candidate/"+str(jobseeker.user_id)
					return JsonResponse({'message': 'Y', 'url': urlval})
				else:
					return JsonResponse({'message': 'Y', 'url': "/"})
			else:
				return JsonResponse({'message': 'X'})
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
		all_login = Login.objects.filter(email = request.POST['email'])
		if(len(all_login)!=0):
			messages.success(request, 'Email address already in use, please enter some other email')
			return redirect('main:index')
		if(request.POST['password']!=request.POST['conpass']):
			messages.error(request, "Both your password and your confirmation password must be exactly same")
			return redirect('main:index')
		if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', request.POST['password']):
			messages.error(request, "Please entere a valid password")
			return redirect('main:index')
		user=Login()
		user.email = request.POST['email']
		user.password = make_password(request.POST['password'])
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
		flag1=True
		for i in request.POST.getlist('experience'):
			if i!="":
				flag1=False
		if(request.POST['mobile']=="" and request.POST['address']=="" and request.POST['dob']=="" and request.POST['basic']=="" and request.POST['master']=="" and request.POST['other']=="" and len(request.POST.getlist('skills'))==0 and flag1==True and len(request.FILES)==0):
			messages.success(request, 'Please enter at least one of the fields')
			return redirect('main:profilecompletion', pk=pk)
		jobseeker=JobSeeker.objects.get(log_id=pk)
		jobseeker.phone=request.POST['code']+request.POST['mobile']
		jobseeker.location=request.POST['address']
		jobseeker.dob=request.POST['dob']
		jobseeker.basic_edu=request.POST['basic']
		jobseeker.master_edu=request.POST['master']
		jobseeker.other_qual=request.POST['other']
		skills = request.POST.getlist('skills')
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
		loger = Login.objects.get(log_id=pk)
		request.session['email'] = loger.email
		request.session['password'] = loger.password
		return redirect("candidate:dashboard", pk=jobseeker.user_id)
	if(len(Login.objects.filter(log_id=pk, user_type="candidate"))==0):
		return redirect('main:index')
	return render(request, 'profile_completion.html')


def emp_completion(request, pk):
	if request.method=="POST":
		if(request.POST['code']=="" and request.POST['mobile']=="" and request.POST['etype']=="" and request.POST['industry']=="" and request.POST['executive']==""  and len(request.FILES)==0 and request.POST['address']=="" and request.POST['pincode']=="" and request.POST['location']=="" and request.POST['profile']==""):
			messages.success(request, 'Please enter at least one of the fields')
			return redirect('main:eprofile', pk=pk)
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
	if(len(Login.objects.filter(log_id=pk, user_type="employer"))==0):
		return redirect('main:index')
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

