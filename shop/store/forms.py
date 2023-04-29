from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserCreateForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class PriceFilterForm(forms.Form):
    min_price = forms.FloatField(required=False)
    max_price = forms.FloatField(required=False)
