from django import forms
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

class Add_customer(forms.Form):
    name = forms.CharField(label=_('First name'), max_length=30, required=False)
    email = forms.EmailField(label=_('Email'), required=False)
    mobile = forms.IntegerField(label=_('Mobile No'), required=True)
    dob = forms.DateField(
        widget=forms.widgets.DateInput(format="%m/%d/%Y"),
        label=_('Date Of Birth'),
        required=False)
    ani = forms.DateField(
        widget=forms.widgets.DateInput(format="%m/%d/%Y"),
        label=_('Date Of Aniversery'),
        required=False)
    area = forms.CharField(label=_('Area'), max_length=255, required=False)
    city = forms.CharField(label=_('City'), max_length=255, required=False)
    subarea = forms.CharField(label=_('Sub_area'), max_length=255, required=False)


class Add_staff(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class Add_branch(forms.Form):
    branch = forms.CharField(label=_('Add Group'), max_length=30, required=True)
