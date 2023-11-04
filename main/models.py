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
    log_id = models.ForeignKey(
        Login, default=None, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, default=None, null=True)
    location = models.CharField(max_length=200, default=None, null=True)
    experience = models.CharField(max_length=100, default=None, null=True)
    skills = models.CharField(max_length=100, default=None, null=True)
    basic_edu = models.CharField(max_length=100, default=None, null=True)
    master_edu = models.CharField(max_length=100, default=None, null=True)
    other_qual = models.CharField(max_length=100, default=None, null=True)
    cursal = models.IntegerField(default=0)
    expsal = models.IntegerField(default=0)
    dob = models.CharField(max_length=50, default=None, null=True)
    Resume = models.FileField(upload_to='resumes/', default=None, null=True)
    photo = models.ImageField(upload_to='photos/', default=None, null=True)
    notice_period = models.CharField(max_length=50, default=None, null=True)
    role = models.CharField(max_length=750, default=None, null=True)
    def pass_to_list(self):
        return self.skills.split(',')

    class Meta:
        db_table = "jobseeker"


class Employer(models.Model):
    eid = models.AutoField(primary_key=True)
    log_id = models.ForeignKey(
        Login, default=None, null=True, on_delete=models.CASCADE)
    ename = models.CharField(max_length=100, default=None, null=True)
    etype = models.CharField(max_length=100, default=None, null=True)
    industry = models.CharField(max_length=100, default=None, null=True)
    address = models.CharField(max_length=200, default=None, null=True)
    pincode = models.CharField(max_length=100, default=None, null=True)
    executive = models.CharField(max_length=100, default=None, null=True)
    phone = models.CharField(max_length=100, default=None, null=True)
    location = models.CharField(max_length=200, default=None, null=True)
    profile = models.CharField(max_length=700, default=None, null=True)
    logo = models.ImageField(
        upload_to='logos/', default=None, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    yearfounded = models.CharField(max_length=10, default=None, null=True)
    size = models.CharField(max_length=20, default=None, null=True)
    city = models.CharField(max_length=30, default=None, null=True)
    fblink = models.CharField(max_length=100, default=None, null=True)
    twlink = models.CharField(max_length=100, default=None, null=True)
    inlink = models.CharField(max_length=100, default=None, null=True)
    lnlink = models.CharField(max_length=100, default=None, null=True)
    cover = models.ImageField(
        upload_to='cover/', default=None, blank=True, null=True)
    about = models.CharField(
        max_length=500, default="Not Specified", null=True)

    class Meta:
        db_table = "employer"


class Admin(models.Model):
    aid = models.AutoField(primary_key=True)
    log_id = models.ForeignKey(
        Login, default=None, null=True, on_delete=models.CASCADE)
    aname = models.CharField(max_length=100, default=None, null=True)
    arole = models.CharField(max_length=100, default=None, null=True)
    phone = models.CharField(max_length=100, default=None, null=True)
    email = models.EmailField(max_length=100, default=None, null=True)
    # profile_picture = models.ImageField(upload_to='admin_profiles/', default=None, blank=True, null=True)

    class Meta:
        db_table = "admin"


class Jobs(models.Model):
    jobid = models.AutoField(primary_key=True)
    eid = models.ForeignKey(Employer, default=None,
                            null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default=None, null=True)
    jobdesc = models.CharField(max_length=700, default=None, null=True)
    vacno = models.IntegerField(default=None, null=True)
    experience = models.CharField(max_length=100, default=None, null=True)
    basicpay = models.CharField(max_length=50, default=None, null=True)
    fnarea = models.CharField(max_length=100, default=None, null=True)
    location = models.CharField(max_length=200, default=None, null=True)
    industry = models.CharField(max_length=200, default=None, null=True)
    ugqual = models.CharField(max_length=100, default=None, null=True)
    pgqual = models.CharField(max_length=100, default=None, null=True)
    profile = models.CharField(max_length=700, default=None, null=True)
    postdate = models.DateTimeField(default=timezone.now)
    jobtype = models.CharField(max_length=50, default="Full Time")
    skills = models.CharField(max_length=700, default=None, null=True)
    notice_period = models.CharField(max_length=50, default=None, null=True)
    responsibilities = models.CharField(
        max_length=700, default=None, null=True)
    requirements = models.CharField(max_length=700, default=None, null=True)
    num_of_visits = models.IntegerField(default=0)
    status = models.IntegerField(default=3)
    suggestions = models.CharField(max_length=2000, default="[]")
    job_desc = models.FileField(upload_to='job_description/', default=None, null=True)

    class Meta:
        db_table = "jobs"


class Selection(models.Model):
    sel_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    emp_id = models.ForeignKey(
        Employer, default=None, null=True, on_delete=models.CASCADE)
    job_id = models.ForeignKey(
        Jobs, default=None, null=True, on_delete=models.CASCADE)
    status = models.IntegerField(default=None, null=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        db_table = "selection"


class ExperienceJob(models.Model):
    exp_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100, default=None, null=True)
    company = models.CharField(max_length=200, default=None, null=True)
    time_period = models.CharField(max_length=50, default=None, null=True)
    description = models.CharField(max_length=500, default=None, null=True)

    class Meta:
        db_table = "experiencejob"


class Education(models.Model):
    edu_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default=None, null=True)
    school = models.CharField(max_length=200, default=None, null=True)
    time_period = models.CharField(max_length=50, default=None, null=True)
    description = models.CharField(max_length=500, default=None, null=True)

    class Meta:
        db_table = "education"


class ProfileVisits(models.Model):
    visit_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        JobSeeker, default=None, null=True, on_delete=models.DO_NOTHING)
    e_id = models.ForeignKey(Employer, default=None,
                             null=True, on_delete=models.DO_NOTHING)
    visiting_time = models.DateTimeField(default=timezone.now)
    user_type = models.CharField(max_length=5, default=None, null=True)

    class Meta:
        db_table = "profilevisits"


class Threads(models.Model):
    msg_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(
        Login, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Login, on_delete=models.CASCADE, related_name='receiver')
    has_unread = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "threads"


class Messages(models.Model):
    msg_id = models.ForeignKey(
        Threads, on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(
        Login, on_delete=models.CASCADE, related_name='sender_user')
    receiver_user = models.ForeignKey(
        Login, on_delete=models.CASCADE, related_name='receiver_user')
    body = models.CharField(max_length=10000)
    image = models.ImageField(upload_to='messages/', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "messages"


class ResumeAnalysis(models.Model):
    any_id = models.AutoField(primary_key=True)
    jobseeker_id = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, blank=True, null=True)
    resume_score = models.CharField(max_length=10, default=None, null=True)
    date = models.DateField(auto_now=True)
    no_of_pages = models.CharField(max_length=5, default=None, null=True)
    predicted_field = models.CharField(max_length=100, default=None, null=True)
    user_level = models.CharField(max_length=100, default=None, null=True)
    actual_skills = models.CharField(max_length=500, default=None, null=True)
    reco_skills = models.CharField(max_length=500, default=None, null=True)
    reco_courses = models.CharField(max_length=1000, default=None, null=True)
    recommendations = models.CharField(
        max_length=1000, default=None, null=True)

    class Meta:
        db_table = "resumeanalysis"


class LikedJobs(models.Model):
    like_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, blank=True, null=True)
    job_id = models.ForeignKey(
        Jobs, on_delete=models.CASCADE, blank=True, null=True)
    likedate = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "likedjobs"


class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "test"
        


class TestInfo(models.Model):
    testinfoid = models.AutoField(primary_key=True)
    test_id = models.ForeignKey(
        Test, on_delete=models.CASCADE, blank=True, null=True)
    test_name = models.CharField(max_length=100, default=None, null=True)
    eid = models.ForeignKey(
        Employer, on_delete=models.CASCADE, default=None, null=True)
    time_limit = models.IntegerField(default=0)

    class Meta:
        db_table = "testinfo"


class TestQues(models.Model):
    ques_id = models.AutoField(primary_key=True)
    testinfoid = models.ForeignKey(
        TestInfo, on_delete=models.CASCADE, blank=True, null=True)
    ques_name = models.CharField(max_length=200, default=None, null=True)
    option1 = models.CharField(max_length=100, default=None, null=True)
    option2 = models.CharField(max_length=100, default=None, null=True)
    option3 = models.CharField(max_length=100, default=None, null=True)
    option4 = models.CharField(max_length=100, default=None, null=True)
    correct = models.IntegerField()
    images = models.ImageField(upload_to='test_images/', default=None, null=True)


    class Meta:
        db_table = "testques"

class Application(models.Model):
    apply_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    eid = models.ForeignKey(Employer, default=None,
                            null=True, on_delete=models.CASCADE)
    job_id = models.ForeignKey(
        Jobs, default=None, null=True, on_delete=models.CASCADE)
    status = models.IntegerField(default=None, null=True)
    date_applied = models.DateTimeField(default=timezone.now)
    test = models.ForeignKey(TestInfo, default=None,
                             blank=True, null=True, on_delete=models.CASCADE)
    why_desc = models.CharField(
        max_length=700, default=None, blank=True, null=True)

    class Meta:
        db_table = "application"

class TestUser(models.Model):
    testuser_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, blank=True, null=True)
    test_id = models.ForeignKey(
        Test, on_delete=models.CASCADE, blank=True, null=True)
    emp_id = models.ForeignKey(
        Employer, on_delete=models.CASCADE, blank=True, null=True)
    correct_answers = models.IntegerField(default=0)
    total_ques = models.IntegerField(default=0)
    answers = models.CharField(max_length=100, default=None, null=True)
    date = models.DateTimeField(default=timezone.now)
    apply_id = models.ForeignKey(
        Application, on_delete=models.CASCADE, blank=True, null=True)
    
    

    class Meta:
        db_table = "testuser"

class Notifications(models.Model):
    notif_id = models.AutoField(primary_key=True)
    send_id = models.ForeignKey(
        Login, on_delete=models.CASCADE, blank=True, null=True, related_name='notif_sender')
    rece_id = models.ForeignKey(
        Login, on_delete=models.CASCADE, blank=True, null=True, related_name='notif_receiver')
    datetime = models.DateTimeField(default=timezone.now)
    notif_type = models.CharField(max_length=10, default=None, null=True)
    readed = models.BooleanField(default=False)
    job_id = models.ForeignKey(
        Jobs, on_delete=models.CASCADE, blank=True, null=True, related_name='notif_job')
    testuser_id = models.ForeignKey(
        TestUser, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "notifications"


class Interview(models.Model):
    int_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, blank=True, null=True)
    eid = models.ForeignKey(
        Employer, on_delete=models.CASCADE, blank=True, null=True)
    apply_id = models.ForeignKey(
        Application, on_delete=models.CASCADE, blank=True, null=True)
    int_link = models.CharField(
        max_length=300, default=None, blank=True, null=True)
    schedule_date = models.DateTimeField(default=timezone.now)
    is_done = models.BooleanField(default=False)
    is_feedgiven = models.BooleanField(default=False)
    cand_feedback = models.CharField(
        max_length=500, default=None, blank=True, null=True)
    testuser_id = models.ForeignKey(
        TestUser, on_delete=models.CASCADE, blank=True, null=True)
    panel_req = models.IntegerField(default=0)

    class Meta:
        db_table = "interview"


class Feedback(models.Model):
    feed_id = models.AutoField(primary_key=True)
    int_id = models.ForeignKey(
        Interview, on_delete=models.CASCADE, blank=True, null=True)
    emp_feedback = models.CharField(
        max_length=500, default=None, blank=True, null=True)
    name = models.CharField(
        max_length=100, default=None, blank=True, null=True)
    rating = models.IntegerField(default=None,null=True,blank=True)

    class Meta:
        db_table = "feedback"

class ResumeFeedback(models.Model):
    feed_id = models.AutoField(primary_key=True)
    job_id = models.ForeignKey(
        Jobs, on_delete=models.CASCADE, blank=True, null=True)
    
    rating = models.IntegerField(default=None,null=True,blank=True)

    class Meta:
        db_table = "Resumefeedback"


class Newsletter(models.Model):
    news_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=300)

    class Meta:
        db_table = "newsletter"


class AllSkills(models.Model):
    id = models.AutoField(primary_key=True)
    skill = models.CharField(max_length=750)

    class Meta:
        db_table = "allskills"


class RoleDetails(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=750)

    class Meta:
        db_table = "roledetails"


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=512)
    description = models.CharField(max_length=512)
    institution_type = models.CharField(max_length=512)

    class Meta:
        db_table = "course"


class Templates(models.Model):
    template_id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=100)
    template_description = models.CharField(max_length=512)
    created_date = models.DateTimeField(default=timezone.now)
    emp_id = models.ForeignKey(Employer, default=None,
                            null=True, on_delete=models.CASCADE)
    class Meta:
        db_table = "templates"


class Steps(models.Model):
    step_id = models.AutoField(primary_key=True)
    step_name = models.CharField(max_length=512)
    step_description = models.CharField(max_length=512)
    created_date = models.DateTimeField(default=timezone.now)
    step_resources = models.CharField(max_length=512)
    step_tasks = models.CharField(max_length=512)
    emp_id = models.ForeignKey(Employer, default=None,
                            null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "steps"


class TemplateSteps(models.Model):
    template_id = models.ForeignKey(Templates, default=None, null=True, on_delete=models.CASCADE)
    step_id = models.ForeignKey(Steps, default=None, null=True, on_delete=models.CASCADE)
    step_order = models.IntegerField(default=None, null=True)

    class Meta:
        db_table = "templatesteps"

class Seminars(models.Model):
    seminar_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    date = models.DateTimeField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=512)
    is_online = models.IntegerField(default=None, null=True)
    web_link = models.CharField(max_length=200)
    image = models.ImageField(upload_to='seminar/', default=None, null=True)
    speaker = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "seminars"



class MockTest(models.Model):
    test_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "mocktest"
        
class MockTestInfo(models.Model):
    testinfoid = models.AutoField(primary_key=True)
    test_id = models.ForeignKey(
        MockTest, on_delete=models.CASCADE, blank=True, null=True)
    test_name = models.CharField(max_length=100, default=None, null=True)
    tech = models.CharField(max_length=100, default=None, null=True)
    time_limit = models.IntegerField(default=0)

    class Meta:
        db_table = "mocktestinfo"

class MockTestQues(models.Model):
    ques_id = models.AutoField(primary_key=True)
    testinfoid = models.ForeignKey(
        MockTestInfo, on_delete=models.CASCADE, blank=True, null=True)
    ques_name = models.CharField(max_length=200, default=None, null=True)
    option1 = models.CharField(max_length=100, default=None, null=True)
    option2 = models.CharField(max_length=100, default=None, null=True)
    option3 = models.CharField(max_length=100, default=None, null=True)
    option4 = models.CharField(max_length=100, default=None, null=True)
    correct = models.IntegerField()
    images = models.ImageField(upload_to='test_images/', default=None, null=True)


    class Meta:
        db_table = "mocktestques"

class CandidateTemplateAssignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    candidate_id = models.ForeignKey(JobSeeker, default=None, null=True, on_delete=models.CASCADE)
    template_id = models.ForeignKey(Templates, default=None, null=True, on_delete=models.CASCADE)
    current_step_order = models.IntegerField(default=None, null=True)
    application_id = models.ForeignKey(Application, default=None, null=True, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "candidatetemplateassignments"


class CandidateStepProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(CandidateTemplateAssignments, default=None, null=True, on_delete=models.CASCADE)
    step_id = models.ForeignKey(Steps, default=None, null=True, on_delete=models.CASCADE)
    is_completed = models.BooleanField()
    completion_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "candidatestepprogress"

