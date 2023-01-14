from django.db import models

class Admin(models.Model):
    adm_id = models.IntegerField()
    adm_name = models.CharField(max_length=100)
    adm_pass = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'admin'


class Application(models.Model):
    apply_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Jobseeker', models.DO_NOTHING, blank=True, null=True)
    emp = models.ForeignKey('Employer', models.DO_NOTHING, blank=True, null=True)
    job = models.ForeignKey('Jobs', models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    date_applied = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'application'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employer(models.Model):
    eid = models.AutoField(primary_key=True)
    log = models.ForeignKey('Login', models.DO_NOTHING)
    ename = models.CharField(max_length=100, blank=True, null=True)
    etype = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=100, blank=True, null=True)
    executive = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile = models.CharField(max_length=700, blank=True, null=True)
    logo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employer'


class Jobs(models.Model):
    jobid = models.AutoField(primary_key=True)
    eid = models.ForeignKey(Employer, models.DO_NOTHING, db_column='eid')
    title = models.CharField(max_length=100, blank=True, null=True)
    jobdesc = models.CharField(max_length=700)
    vacno = models.IntegerField(blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    basicpay = models.CharField(max_length=100, blank=True, null=True)
    fnarea = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=200, blank=True, null=True)
    ugqual = models.CharField(max_length=100, blank=True, null=True)
    pgqual = models.CharField(max_length=100, blank=True, null=True)
    profile = models.CharField(max_length=700, blank=True, null=True)
    postdate = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'jobs'


class Jobseeker(models.Model):
    user_id = models.AutoField(primary_key=True)
    log = models.ForeignKey('Login', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=100, blank=True, null=True)
    basic_edu = models.CharField(max_length=100, blank=True, null=True)
    master_edu = models.CharField(max_length=100, blank=True, null=True)
    other_qual = models.CharField(max_length=100, blank=True, null=True)
    dob = models.CharField(max_length=50, blank=True, null=True)
    resume = models.CharField(db_column='Resume', max_length=100, blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobseeker'


class Login(models.Model):
    log_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    usertype = models.CharField(max_length=20)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'login'


class Selection(models.Model):
    sel_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Jobseeker, models.DO_NOTHING, blank=True, null=True)
    emp = models.ForeignKey(Employer, models.DO_NOTHING, blank=True, null=True)
    job = models.ForeignKey(Jobs, models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'selection'

