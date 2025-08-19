from celery import shared_task
from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER


@shared_task
def send_code_to_email(email, code):
    subject = 'Email Verification'
    message = f'Your verification code is: {code}'
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
