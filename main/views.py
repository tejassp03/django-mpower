from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import JobSeeker, Login, Employer, ResumeAnalysis, Jobs, LikedJobs, Application, Interview, Feedback, Newsletter
import random
import re
from django.contrib.auth.hashers import make_password, check_password

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count


import pandas as pd
import time
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from PIL import Image
from .Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
# import plotly.express as px


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain

from django.db.models import Q
from django.db.models import Max, Min

from json import dumps



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
						urlval="/profile_completion/"+str(user[0].log_id)
						return JsonResponse({'message': 'Y', 'url': urlval})
					# return redirect('main:profilecompletion', pk=user[0].log_id)
				elif(request.POST['user'] == 'employer' and Employer.objects.filter(log_id=user[0].log_id)):
					employer=Employer.objects.get(log_id=user[0].log_id)
					if((employer.etype==None or employer.etype=="") and (employer.industry==None or employer.industry=="") and (employer.address==None or employer.address=="") and (employer.pincode==None or employer.pincode=="") and (employer.executive==None or employer.executive=="") and (employer.phone==None or employer.phone=="" or len(employer.phone)<=4) and (employer.location==None or employer.location=="") and (employer.profile==None or employer.profile=="") and (employer.logo=="" or employer.logo==None)):
						urlval="/emp_completion/"+str(user[0].log_id)
						return JsonResponse({'message': 'Y', 'url': urlval})
				else:
					return JsonResponse({'message': 'X'})
				request.session['email'] = request.POST['c_email']
				request.session['password'] = user[0].password
				user[0].status=1
				user[0].save()
				if(request.POST['user'] == 'candidate'):
					empls=JobSeeker.objects.get(log_id=user[0].log_id)
					request.session['name']=empls.name
					request.session['pk']=empls.user_id
					request.session['type']="c"
					if(empls.photo):
						request.session['photo']=empls.photo.url
					urlval="/candidate/"+str(jobseeker.user_id)
					return JsonResponse({'message': 'Y', 'url': urlval})
				else:
					emp=Employer.objects.get(log_id=user[0].log_id)
					request.session['name']=emp.ename
					request.session['pk']=emp.eid
					request.session['type']="e"
					if(emp.logo):
						request.session['photo']=emp.logo.url
					urlval="/employer/"+str(emp.eid)
					return JsonResponse({'message': 'Y', 'url': urlval})
			else:
				return JsonResponse({'message': 'X'})
	jobs=Jobs.objects.all()
	typ=jobs.values('fnarea').annotate(Count('fnarea')).order_by('-fnarea__count')
	applics=Application.objects.values('job_id').annotate(Count('job_id')).order_by('-job_id__count')
	coms=jobs.values('eid').annotate(Count('eid')).order_by('-eid__count')
	vals=[]
	co=0
	for i in typ:
		if(co>5):
			break
		single_val={}
		single_val['fnarea']=i['fnarea']
		single_val['count']=i['fnarea__count']
		vals.append(single_val)
		co=co+1
	locations=jobs.order_by().values('location').distinct()
	titles=jobs.order_by().values('title').distinct()
	title=[]
	locate=[]
	jobs_info=[]
	co=0
	for i in applics:
		if(co>7):
			break
		single_j={}
		sin=Jobs.objects.get(jobid=i['job_id'])
		single_j['fnarea']=sin.fnarea
		single_j['title']=sin.title
		single_j['location']=sin.location
		single_j['type']=sin.jobtype
		single_j['date']=sin.postdate
		single_j['name']=sin.eid.ename
		if(sin.eid.logo):
			single_j['logo']=sin.eid.logo
		else:
			single_j['logo']=None
		single_j['eid']=sin.eid.eid
		jobs_info.append(single_j)
		co=co+1
	coms_info=[]
	for i in coms:
		single_com={}
		emp=Employer.objects.get(eid=i['eid'])
		single_com['name']=emp.ename
		single_com['eid']=emp.eid
		if(emp.logo):
			single_com['logo']=emp.logo
		else:
			single_com['logo']=None
		single_com['info']=emp.profile
		single_com['count']=i['eid__count']
		coms_info.append(single_com)
	for i in titles:
		title.append(i['title'])
	for i in locations:
		locate.append(i['location'])
	return render(request, 'index.html', {'locations': locations, 'titles': titles, 'title': dumps(title), 'vals': vals, 'jobs': jobs_info, 'coms': coms_info, 'loc': locate, 'total': len(jobs)})

def view_function(request):
    messages.add_message(request, messages.INFO, 'This is an info message')
    messages.add_message(request, messages.ERROR, 'This is an error message')
    return redirect('main:index')

def subscribe(request):
	if request.method=="POST":
		temp=Newsletter.objects.filter(email=request.POST['news_email'])
		if(len(temp)>0):
			messages.error(request, 'Email already exists')
			return redirect('main:index')
		news=Newsletter()
		news.email=request.POST['news_email']
		news.save()
		messages.error(request, 'Subscription added')
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
		jobs=jobs.filter(basicpay__in=request.GET.getlist('sal'))
		sal_sel=request.GET.getlist('sal')
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
	jobtype=jobs.order_by().values('jobtype').distinct()
	emptype=jobs.order_by().values('experience').distinct()
	salary=jobs.order_by('basicpay').values('basicpay').distinct()
	countjob=[]
	countemp=[]
	countsal=[]
	for i in jobtype:
		countjob.append(len(jobs.filter(jobtype=i['jobtype'])))
	for i in emptype:
		countemp.append(len(jobs.filter(experience=i['experience'])))
	for i in salary:
		countsal.append(len(jobs.filter(basicpay=i['basicpay'])))
	context={'c': c_val, 'l': l_val, 't': t_val, 'd': d_val, 'sel': emp_sel, 'eel': exp_sel, 'els': sal_sel}
	return render(request, 'jobs.html', {'page_obj': page_obj, 'pe': page_obj, 'count': count, 'locations': locations, 'titles': titles, 'categories': categories, 'GET_params':GET_params, 'jobtype': zip(jobtype, countjob), 'emptype': zip(emptype, countemp), 'saltype': zip(salary, countsal), 'context': context})

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
		for i in skills:
			all_skills=all_skills+i+","
		experiences = request.POST.get('experience')
		jobseeker.skills=all_skills
		jobseeker.experience=experiences
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
		request.session['type']="c"
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
		loger.status=1
		loger.save()
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
    c = 0
    rec_course = []
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        rec_course.append(c_name)
        if c == 4:
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
		loger=Login.objects.get(log_id=pk)
		request.session['email'] = loger.email
		request.session['password'] = loger.password
		request.session['name']=employer.ename
		request.session['pk']=employer.eid
		request.session['type']="e"
		if(employer.logo):
			request.session['photo']=employer.logo.url
		loger.status=1
		loger.save()
		return redirect("employer:cdashboard", pk=employer.eid)
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
	jobdet.num_of_visits=jobdet.num_of_visits+1
	jobdet.save()
	lik=False
	app_date=None
	companydet=Employer.objects.get(eid=jobdet.eid.eid)
	if 'pk' in request.session:
		liked=LikedJobs.objects.filter(job_id=pk2, user_id=request.session['pk'])
		if liked:
			lik=True
		applics=Application.objects.filter(job_id=pk2, user_id=request.session['pk'])
		if applics:
			app_date=applics[0].date_applied
	loger=Login.objects.get(log_id=companydet.log_id.log_id)
	skills=[]
	for i in jobdet.skills.split("\n"):
		skills.append(i)
	requirements=[]
	for i in jobdet.requirements.split("\n"):
		requirements.append(i)
	responsibilities=[]
	for i in jobdet.responsibilities.split("\n"):
		responsibilities.append(i)
	return render(request, 'singlejob.html', {'job_details': jobdet, 'company_details': companydet, 'liked': lik, 'loger': loger, 'skills': skills, 'requirements': requirements, 'responsibilities': responsibilities, 'date': app_date})

def singlecompany(request, pk2):
	cominfo=Employer.objects.get(eid=pk2)
	jobs=Jobs.objects.filter(eid=cominfo.eid).order_by('-postdate')
	return render(request, 'singlecompany.html', {'cominfo': cominfo, 'jobs': jobs})

def get_job(request):
	if(request.method=="GET"):
		job=Jobs.objects.get(jobid=request.GET['id'])
		return JsonResponse({'name': job.title, 'id': job.jobid})
	if(request.method=="POST"):
		applic=Application()
		applic.user_id=JobSeeker.objects.get(user_id=request.session['pk'])
		applic.status=0
		applic.job_id=Jobs.objects.get(jobid=request.POST['id'])
		applic.eid=applic.job_id.eid
		applic.why_desc=request.POST['whyhire']
		applic.save()
		return JsonResponse({'message': 'Y'})

def give_feedback(request, pk):
	if request.method=="POST":
		int_val=Interview.objects.get(int_id=pk)
		int_val.is_feedgiven=1
		int_val.save()
		feedback=Feedback()
		feedback.int_id=int_val
		feedback.emp_feedback=request.POST['feedback']
		feedback.name=request.POST['name']
		feedback.save()
		messages.error(request, "Feedback successfully recorded!")
		return redirect('main:give_feedback', pk=pk)
	int_val=Interview.objects.get(int_id=pk)
	data={}
	data['name']=int_val.user_id.name
	data['location']=int_val.user_id.location
	data['title']=int_val.user_id.title
	if int_val.user_id.photo:
		data['photo']=int_val.user_id.photo
	return render(request, 'give_feedback.html', {'data': data})

def give_feed(request, pk):
	if request.method=="POST":
		int_val=Interview.objects.get(int_id=pk)
		int_val.cand_feedback=request.POST['feedback']
		int_val.save()
		return redirect("main:index")
	int_val=Interview.objects.get(int_id=pk)
	data={}
	data['ename']=int_val.eid.ename
	data['location']=int_val.eid.location
	if int_val.eid.logo:
		data['logo']=int_val.eid.logo.url
	return render(request, 'give_feed.html', {'data': data})