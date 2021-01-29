from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render

class HomePage(TemplateView):
    template_name = 'index.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'

def send_email(request):
    if request.method == 'POST':
        template = render_to_string('email_template.html',{
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['olga.kiseleva.pro@gmail.com'],
        )
        email.fail_silently = False
        email.send()
    return render(request, 'email_sent.html')