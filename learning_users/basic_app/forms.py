from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput())

    class Meta():
        model = User
        fields = ("username","email","password")
        ## These are the fields that u wanna use from BASE User
        ## U can also exclude any if u dont want

class UserProfileInfoForms(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ("portfolio_site", "profile_pic")
