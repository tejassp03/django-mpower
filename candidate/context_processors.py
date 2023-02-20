from main.models import Notifications, JobSeeker, Employer, Jobs
def notifs(request):
    if len(request.session.keys())!=0:
        if(request.session['type']=="c"):
            emp=JobSeeker.objects.get(user_id=request.session['pk'])
            notifs=Notifications.objects.filter(rece_id=emp.log_id, readed=0).order_by('-datetime')
            request.session['notifnum']=len(notifs)
            data=[]
            for i in notifs:
                new_data={}
                job=Employer.objects.get(log_id=i.send_id)
                new_data['ename']=job.ename
                new_data['datetime']=i.datetime
                new_data['eid']=job.eid
                new_data['notif_type']=i.notif_type
                new_data['log_id']=job.log_id.log_id
                data.append(new_data)
            return {
                'notis' : data
            }
        else:
            emp=Employer.objects.get(eid=request.session['pk'])
            notifs=Notifications.objects.filter(rece_id=emp.log_id, readed=0).order_by('-datetime')
            request.session['notifnum']=len(notifs)
            data=[]
            for i in notifs:
                new_data={}
                cand=JobSeeker.objects.get(log_id=i.send_id)
                new_data['name']=cand.name
                new_data['datetime']=i.datetime
                new_data['user_id']=cand.user_id
                new_data['notif_type']=i.notif_type
                new_data['log_id']=cand.log_id.log_id
                if i.job_id:
                    jobs = Jobs.objects.get(jobid=i.job_id.jobid)
                    new_data['title']=jobs.title
                    new_data['jobid']=jobs.jobid
                data.append(new_data)
            return {
                'notis' : data
            }
    return {}