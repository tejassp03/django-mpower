from django.conf import settings
from django.core.mail import send_mail
def send_emails(subj, mess, receipt):
    subject = subj
    message = mess
    email_from = settings.EMAIL_HOST_USER
    recipient_list = receipt
    send_mail( subject, message, email_from, recipient_list )