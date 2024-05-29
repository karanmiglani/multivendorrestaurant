from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template import TemplateDoesNotExist

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role == None and user.is_superuser:
        redirectUrl = '/admin'
        return redirectUrl


def send_verification_mail(request , user , mail_subject , template_name):
    try:
        current_site = get_current_site(request)
        mail_subject = mail_subject
        message = render_to_string(template_name,{
        'user':user,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user)
    })
        to_email = user.email
        mail = EmailMessage(mail_subject , message,to=[to_email])
        mail.send()
    except TemplateDoesNotExist as e:
        print(f"Template {template_name} doesnot exist")



def send_password_reset_email(request , user):
    current_site = get_current_site(request)
    mail_subject = 'Reset your password'
    message = render_to_string('accounts/emails/reset_password_email.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    to_email = user.email
    mail = EmailMessage(mail_subject , message , to=[to_email])
    mail.send()