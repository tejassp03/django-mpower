from django.db import models
from django.utils import timezone
    
# Create your models here.

class Login(models.Model):
    log_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    user_type = models.CharField(max_length=20)
    status = models.IntegerField(default=None, null=True)
    def __str__(self):
        return str(self.log_id)
    class Meta:
        db_table = "login"


class JobSeeker(models.Model):
    user_id = models.AutoField(primary_key=True)
    log_id = models.ForeignKey(Login, default=None, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, default=None, null=True)
    location = models.CharField(max_length=200, default=None, null=True)
    experience = models.CharField(max_length=100, default=None, null=True)
    skills = models.CharField(max_length=100, default=None, null=True)
    basic_edu = models.CharField(max_length=100, default=None, null=True)
    master_edu = models.CharField(max_length=100, default=None, null=True)
    other_qual = models.CharField(max_length=100, default=None, null=True)
    dob = models.CharField(max_length=50, default=None, null=True)
    Resume = models.FileField(upload_to='resumes/', default=None, null=True)
    photo = models.ImageField(upload_to='photos/', default=None, null=True)
    title = models.CharField(max_length=200, default=None, null=True)
    about = models.CharField(max_length=700, default=None, null=True)
    def pass_to_list(self):
        return self.skills.split(',')
    class Meta:
        db_table = "jobseeker"

class Employer(models.Model):
    eid = models.AutoField(primary_key=True)
    log_id = models.ForeignKey(Login, default=None, null=True, on_delete=models.CASCADE)
    ename = models.CharField(max_length=100, default=None, null=True)
    etype = models.CharField(max_length=100, default=None, null=True)
    industry = models.CharField(max_length=100, default=None, null=True)
    address = models.CharField(max_length=200, default=None, null=True)
    pincode = models.CharField(max_length=100, default=None, null=True)
    executive = models.CharField(max_length=100, default=None, null=True)
    phone = models.CharField(max_length=100, default=None, null=True)
    location = models.CharField(max_length=200, default=None, null=True)
    profile = models.CharField(max_length=700, default=None, null=True)
    logo = models.ImageField(upload_to='logos/', default=None, null=True)
    class Meta:
        db_table = "employer"

class Jobs(models.Model):
    jobid = models.AutoField(primary_key=True)
    eid = models.ForeignKey(Employer, default=None, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default=None, null=True)
    jobdesc = models.CharField(max_length=700, default=None, null=True)
    vacno = models.IntegerField(default=None, null=True)
    experience = models.CharField(max_length=100, default=None, null=True)
    basicpay = models.CharField(max_length=100, default=None, null=True)
    fnarea = models.CharField(max_length=100, default=None, null=True)
    location = models.CharField(max_length=200, default=None, null=True)
    industry = models.CharField(max_length=200, default=None, null=True)
    ugqual = models.CharField(max_length=100, default=None, null=True)
    pgqual = models.CharField(max_length=100, default=None, null=True)
    profile = models.CharField(max_length=700, default=None, null=True)
    postdate = models.DateField(default=timezone.now)
    class Meta:
        db_table = "jobs"

class Application(models.Model):
    apply_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    emp_id = models.ForeignKey(Employer, default=None, null=True, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Jobs, default=None, null=True, on_delete=models.CASCADE)
    status = models.IntegerField(default=None, null=True)
    date_applied = models.DateField(default=timezone.now)
    class Meta:
        db_table = "application"

class Selection(models.Model):
    sel_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    emp_id = models.ForeignKey(Employer, default=None, null=True, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Jobs, default=None, null=True, on_delete=models.CASCADE)
    status = models.IntegerField(default=None, null=True)
    date = models.DateField(default=timezone.now)
    class Meta:
        db_table = "selection"

class ExperienceJob(models.Model):
    exp_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100, default=None, null=True)
    company = models.CharField(max_length=200, default=None, null=True)
    time_period = models.CharField(max_length=50, default=None, null=True)
    description = models.CharField(max_length=500, default=None, null=True)
    class Meta:
        db_table = "experiencejob"

class Education(models.Model):
    edu_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default=None, null=True)
    school = models.CharField(max_length=200, default=None, null=True)
    time_period = models.CharField(max_length=50, default=None, null=True)
    description = models.CharField(max_length=500, default=None, null=True)
    class Meta:
        db_table = "education"

class ProfileVisits(models.Model):
    visit_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(JobSeeker, default=None, null=True, on_delete=models.DO_NOTHING)
    e_id = models.ForeignKey(Employer, default=None, null=True, on_delete=models.DO_NOTHING)
    visiting_time = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "profilevisits"
    
class Threads(models.Model):
    msg_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='receiver')
    has_unread = models.BooleanField(default=False)
    class Meta:
        db_table = "threads"

class Messages(models.Model):
    msg_id = models.ForeignKey(Threads, on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='sender_user')
    receiver_user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='receiver_user')
    body = models.CharField(max_length=10000)
    image = models.ImageField(upload_to='messages/', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    class Meta:
        db_table = "messages"

