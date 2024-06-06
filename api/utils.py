from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags




def send_booking_ref_to_client(id, email, text, subject):
    html_message = render_to_string('email_template.html', {
        'ref_number': id,
        'booking_message': text
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
    subject,
    plain_message,
    settings.EMAIL_HOST_USER,
    email,
    fail_silently=False,
    html_message=html_message
    )   
    