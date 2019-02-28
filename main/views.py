from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from mgmt.models import *
from django.conf import settings
from django.contrib import messages

def index(request):
    l = Customer.objects.all().filter(owner=request.user)
    return render(request, 'main/index.html', {
            'Customer':l,
    })


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
