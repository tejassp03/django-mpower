from main.models import Notifications, JobSeeker, Employer
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
                data.append(new_data)
            return {
                'notis' : data
            }
    return {}