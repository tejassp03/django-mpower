from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import JobSeeker, Login, Employer, ResumeAnalysis, Jobs, LikedJobs
import random
import re
from django.contrib.auth.hashers import make_password, check_password

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import streamlit as st
import pandas as pd
import time
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from .Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import plotly.express as px


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain

from django.db.models import Q
from django.db.models import Max, Min


@csrf_exempt
def index(request):
	if request.method == 'POST':
		user=Login.objects.filter(email=request.POST['c_email'])
		if(len(user)==0):
			return JsonResponse({'message': 'X'})
		else:
			if(check_password(request.POST['c_pass'], user[0].password)):
				if(request.POST['user'] == 'candidate' and JobSeeker.objects.filter(log_id=user[0].log_id)):
					jobseeker=JobSeeker.objects.get(log_id=user[0].log_id)
					if((jobseeker.phone==None or jobseeker.phone=="" or len(jobseeker.phone)<=4) and (jobseeker.location==None or jobseeker.location=="") and (jobseeker.experience==None or jobseeker.experience=="") and (jobseeker.skills==None or jobseeker.skills=="") and (jobseeker.basic_edu==None or jobseeker.basic_edu=="") and (jobseeker.master_edu==None or jobseeker.master_edu=="") and (jobseeker.other_qual==None or jobseeker.other_qual=="") and (jobseeker.dob==None or jobseeker.dob=="") and (jobseeker.Resume=="" or jobseeker.Resume==None) and (jobseeker.photo=="" or jobseeker.photo==None)):
						urlval="profile_completion/"+str(user[0].log_id)
						return JsonResponse({'message': 'Y', 'url': urlval})
					# return redirect('main:profilecompletion', pk=user[0].log_id)
				elif(request.POST['user'] == 'employer' and Employer.objects.filter(log_id=user[0].log_id)):
					employer=Employer.objects.get(log_id=user[0].log_id)
					if((employer.etype==None or employer.etype=="") and (employer.industry==None or employer.industry=="") and (employer.address==None or employer.address=="") and (employer.pincode==None or employer.pincode=="") and (employer.executive==None or employer.executive=="") and (employer.phone==None or employer.phone=="" or len(employer.phone)<=4) and (employer.location==None or employer.location=="") and (employer.profile==None or employer.profile=="") and (employer.logo=="" or employer.logo==None)):
						urlval="emp_completion/"+str(user[0].log_id)
						return JsonResponse({'message': 'Y', 'url': urlval})
				else:
					return JsonResponse({'message': 'X'})
				request.session['email'] = request.POST['c_email']
				request.session['password'] = user[0].password
				empls=JobSeeker.objects.get(log_id=user[0].log_id)
				request.session['name']=empls.name
				request.session['pk']=empls.user_id
				if(empls.photo):
					request.session['photo']=empls.photo.url
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
	t_val=""
	c_val=""
	l_val=""
	d_val=""
	emp_sel=[]
	exp_sel=[]
	sal_sel=[]
	data=[]
	if(('title' not in request.GET) and ('category' not in request.GET) and ('location' not in request.GET)):
		jobs=Jobs.objects.all().order_by('-postdate')
	elif(request.GET['title']=="all" and request.GET['location']=="all" and request.GET['category']=="all"):
		jobs=Jobs.objects.all()
	elif(request.GET['location']=="all" and request.GET['category']=="all"):
		jobs=Jobs.objects.filter(title=request.GET['title'])
		t_val=request.GET['title']
	elif(request.GET['title']=="all" and request.GET['category']=="all"):
		jobs=Jobs.objects.filter(location=request.GET['location'])
		l_val=request.GET['location']
	elif(request.GET['title']=="all" and request.GET['location']=="all"):
		jobs=Jobs.objects.filter(fnarea=request.GET['category'])
		c_val=request.GET['category']
	elif(request.GET['title']=="all"):
		jobs=Jobs.objects.filter(location=request.GET['location'], fnarea=request.GET['category'])
		l_val=request.GET['location']
		c_val=request.GET['category']
	elif(request.GET['location']=="all"):
		jobs=Jobs.objects.filter(title=request.GET['title'], fnarea=request.GET['category'])
		t_val=request.GET['title']
		c_val=request.GET['category']
	elif(request.GET['category']=="all"):
		jobs=Jobs.objects.filter(title=request.GET['title'], location=request.GET['location'])
		t_val=request.GET['title']
		l_val=request.GET['location']
	else:
		jobs=Jobs.objects.filter(title=request.GET['title'], location=request.GET['location'], fnarea=request.GET['category'])
		t_val=request.GET['title']
		l_val=request.GET['location']
		c_val=request.GET['category']
	if 'emp' in request.GET:
		jobs=jobs.filter(jobtype__in=request.GET.getlist('emp'))
		emp_sel=request.GET.getlist('emp')
	if 'exp' in request.GET:
		jobs=jobs.filter(experience__in=request.GET.getlist('exp'))
		exp_sel=request.GET.getlist('exp')
	if 'sal' in request.GET:
		minval=-1
		maxval=-1
		for i in request.GET.getlist('sal'):
			ab=i.split(',')
			if int(ab[0])<minval:
				minval=int(ab[0])
			if int(ab[1])>maxval:
				maxval=int(ab[1])
			sal_sel.append([int(ab[0]), int(ab[1])])
		jobs=jobs.filter(basicpay__range=(minval, maxval))
	if 'datesort' in request.GET:
		d_val=request.GET['datesort']
		if(request.GET['datesort']=="2"):
			jobs=jobs.reverse()
	GET_params = request.GET.copy()
	if('page' in GET_params):
		last=GET_params['page'][-1]
		GET_params['page']=last[0]
	count=len(jobs)
	companies=[]
	for i in jobs:
		new_data={}
		new_data['jobid']=i.jobid
		new_data['title']=i.title
		new_data['location']=i.location
		new_data['experience']=i.experience
		new_data['fnarea']=i.fnarea
		new_data['postdat']=i.postdate
		companies.append(Employer.objects.get(eid=i.eid.eid))
		em=Employer.objects.get(eid=i.eid.eid)
		new_data['eid']=em.eid
		new_data['ename']=em.ename
		new_data['logo']=em.logo
		data.append(new_data)
	p=Paginator(data, 5)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	categories=jobs.order_by().values('fnarea').distinct()
	locations=jobs.order_by().values('location').distinct()
	titles=jobs.order_by().values('title').distinct()
	jobtype=Jobs.objects.order_by().values('jobtype').distinct()
	emptype=Jobs.objects.order_by().values('experience').distinct()
	max_sal=Jobs.objects.all().aggregate(Max('basicpay'))
	min_sal=Jobs.objects.all().aggregate(Min('basicpay'))
	saltype=[]
	diff=None
	if(count!=0):
		diff=(max_sal['basicpay__max']-min_sal['basicpay__min'])//5
		if(diff==0):
			saltype.append([0, 1000*round(min_sal['basicpay__min']/1000)])
		else:
			for i in range(0,5):
				if saltype:
					if saltype[-1][1]!=1000*round((saltype[-1][1]+diff)/1000):
						saltype.append([saltype[-1][1], 1000*round((saltype[-1][1]+diff)/1000)])
				else:
					saltype.append([0, 1000*round(min_sal['basicpay__min']/1000)])
					if 1000*round(min_sal['basicpay__min']/1000)!=1000*round((min_sal['basicpay__min']+diff)/1000):
						saltype.append([1000*round(min_sal['basicpay__min']/1000), 1000*round((min_sal['basicpay__min']+diff)/1000)])
	countjob=[]
	countemp=[]
	countsal=[]
	for i in jobtype:
		countjob.append(len(Jobs.objects.filter(jobtype=i['jobtype'])))
	for i in emptype:
		countemp.append(len(Jobs.objects.filter(experience=i['experience'])))
	for i in saltype:
		countsal.append(len(Jobs.objects.filter(basicpay__range=(i[0], i[1]))))
	context={'c': c_val, 'l': l_val, 't': t_val, 'd': d_val, 'sel': emp_sel, 'eel': exp_sel, 'els': sal_sel}
	return render(request, 'jobs.html', {'page_obj': page_obj, 'pe': page_obj, 'count': count, 'locations': locations, 'titles': titles, 'categories': categories, 'GET_params':GET_params, 'jobtype': zip(jobtype, countjob), 'emptype': zip(emptype, countemp), 'saltype': zip(saltype, countsal), 'context': context})

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
		empls=JobSeeker.objects.get(log_id=pk)
		request.session['name']=empls.name
		request.session['pk']=empls.user_id
		if(empls.Resume):
			analysis_object = ResumeAnalysis()
			analysis_object.jobseeker_id = empls
			resume_data = ResumeParser("media/"+str(empls.Resume)).get_extracted_data()
			if resume_data:
				resume_text = pdf_reader("media/"+str(empls.Resume))
				try:
					analysis_object.no_of_pages=resume_data['no_of_pages']
					# print(resume_data['name'], resume_data['email'], resume_data['mobile_number'], str(resume_data['no_of_pages']))
				except:
					print("!")
				cand_level = ''
				if resume_data['no_of_pages'] == 1:
					cand_level = "Fresher"
				elif resume_data['no_of_pages'] == 2:
					cand_level = "Intermediate"
				elif resume_data['no_of_pages'] >=3:
					cand_level = "Experienced"
				if(cand_level):
					analysis_object.user_level=cand_level
				if(resume_data['skills']):
					final=""
					for i in resume_data['skills']:
						if(i!=""):
							final=final+","+i
					analysis_object.actual_skills=final
				# print(resume_data['skills'])
				ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
				web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
					'javascript', 'angular js', 'c#', 'flask']
				android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
				ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
				uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']

				recommended_skills = []
				reco_field = ''
				rec_course = ''
				for i in resume_data['skills']:
                    ## Data science recommendation
					if i.lower() in ds_keyword:
						# print(i.lower())
						reco_field = 'Data Science'
						recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
						rec_course = course_recommender(ds_course)
						break

					## Web development recommendation
					elif i.lower() in web_keyword:
						# print(i.lower())
						reco_field = 'Web Development'
						recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
						rec_course = course_recommender(web_course)
						break

					## Android App Development
					elif i.lower() in android_keyword:
						# print(i.lower())
						reco_field = 'Android Development'
						recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
						rec_course = course_recommender(android_course)
						break

					## IOS App Development
					elif i.lower() in ios_keyword:
						# print(i.lower())
						reco_field = 'IOS Development'
						recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
						rec_course = course_recommender(ios_course)
						break

					## Ui-UX Recommendation
					elif i.lower() in uiux_keyword:
						# print(i.lower())
						reco_field = 'UI-UX Development'
						recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
						rec_course = course_recommender(uiux_course)
						break
				if(reco_field):
					analysis_object.predicted_field=reco_field
				if(recommended_skills):
					final=""
					for i in recommended_skills:
						if(i!=""):
							final=final+","+i
					analysis_object.reco_skills=final
				if(rec_course):
					final=""
					for i in rec_course:
						if(i!=""):
							final=final+","+i
					analysis_object.reco_courses=final
				resume_score = 0
				recommendations=[]
				if 'Objective' in resume_text:
					resume_score = resume_score+20
					recommendations.append('Awesome! You have added Objective')
					# print("Objectives added good")
				else:
					recommendations.append('According to our recommendation please add your career objective, it will give your career intension to the Recruiters')
					# print("According to our recommendation please add your career objective, it will give your career intension to the Recruiters")
				if 'Declaration'  in resume_text:
					resume_score = resume_score + 20
					recommendations.append('Awesome! You have added Declaration')
					# print("Declaration added good")
				else:
					recommendations.append('According to our recommendation please add Declaration. It will give the assurance that everything written on your resume is true and fully acknowledged by you')
					# print("According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you")
				if 'Hobbies' or 'Interests'in resume_text:
					resume_score = resume_score + 20
					recommendations.append('Awesome! You have added Hobbies')
					# print("Hobbies or interests are added good")
				else:
					recommendations.append("According to our recommendation please add Hobbies. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.")
					# print("According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.")
				if 'Achievements' in resume_text:
					resume_score = resume_score + 20
					recommendations.append("Awesome! You have added Achievements")
					# print("Achievements added good")
				else:
					recommendations.append("According to our recommendation please add Achievements. It will show that you are capable for the required position.")
					# print("According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.")
				if 'Projects' in resume_text:
					resume_score = resume_score + 20
					recommendations.append("Awesome! You have added Projects")
					# print("Projects added good")
				else:
					recommendations.append("According to our recommendation please add Projects. It will show that you have done work related the required position or not.")
					# print("According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.")
				score = 0
				for percent_complete in range(resume_score):
					score +=1
					time.sleep(0.1)
				analysis_object.resume_score=score
				final=""
				for i in recommendations:
					if(i!=""):
						final=final+","+i
				analysis_object.recommendations=final
				analysis_object.save()
				# print("Your resume score: ", score)
		if(empls.photo):
			request.session['photo']=empls.photo.url
		return redirect("candidate:dashboard", pk=jobseeker.user_id)
	if(len(Login.objects.filter(log_id=pk, user_type="candidate"))==0):
		return redirect('main:index')
	return render(request, 'profile_completion.html')

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


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

def get_otp(request, pk):
	if request.method == "GET":
		key = base64.b32encode(returnvalue(request.GET['phone']).encode())
		OTP = pyotp.TOTP(key,interval = 30)
		return JsonResponse({'OTP': OTP.now()})
	return JsonResponse({'OTP': 'X'})

def verify_otp(request, pk):
	if(request.method=='POST'):
		key = base64.b32encode(returnvalue(request.POST['phone']).encode())
		OTP = pyotp.TOTP(key,interval = 30)
		if OTP.verify(int(request.POST['OTP'])):
			return JsonResponse({'message': 'Phone number verified'})
	return JsonResponse({'message': 'Please enter correct OTP'})


def singlejob(request, pk2):
	if request.method=="POST":
		like=LikedJobs()
		like.job_id=Jobs.objects.get(jobid=pk2)
		like.user_id=JobSeeker.objects.get(user_id=request.session['pk'])
		like.save()
		return redirect('main:singlejob', pk2=pk2)
	jobdet=Jobs.objects.get(jobid=pk2)
	companydet=Employer.objects.get(eid=jobdet.eid.eid)
	liked=LikedJobs.objects.filter(job_id=pk2)
	return render(request, 'singlejob.html', {'job_details': jobdet, 'company_details': companydet, 'liked': liked})

