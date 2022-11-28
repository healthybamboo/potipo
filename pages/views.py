from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class TermsOfService(TemplateView):
    template_name = 'pages/terms_of_service.html'

class MessageFromManager(TemplateView):
    template_name = 'pages/message_from_manager.html'
