from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
import json
import time
import datetime
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, get_connection
from django.utils.html import strip_tags
from django.conf import settings
from celery import shared_task

User=get_user_model()

@shared_task
def send_verification_mail(email,activation_link, recipient):
    template_name='muse/activate_account_email.html'
    html_content =render_to_string(template_name, context={'email':email, 'activation_link':activation_link})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        'TheMuseAI - Verify Email',
        text_content,
        'no-reply@themuseai.com' ,
        [recipient],
        #fail_silently=False,
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    #return HttpResponse("Email Sent successfully")
    
@shared_task
def welcome_email(user_email):
    template_name='chatrep/welcome.html'
    html_content =render_to_string(template_name, context={'email':user_email, 'credits':25, 'pages':350})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Welcome to TheMuseAI!',
        text_content,
        'noreply@filesquery.com' ,
        [user_email],
        #fail_silently=False,
    )
    email.attach_alternative(html_content, 'text/html')
    time.sleep(5)
    email.send()
    return f'Welcome email sent to {user_email} successfully'

