from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from login.models import User


def isValidUsername(account_name):
    try:
        User.objects.get(account_name=account_name)
    except User.DoesNotExist:
        return
    raise validators.ValidationError('The username "%s" is already taken.' % account_name)

def alreadyExistsEmail(email):
    try:
        User.objects.filter(email=email).exists()
    except User.DoesNotExist:
        return
    raise ValidationError("Email %s already exists" % email)

def existsEmail(email):
    try:
        User.objects.filter(email=email).exists()
    except User.DoesNotExist:
        raise ValidationError("Email %s already exists" % email)

def identicalPasswords(password, password2):
    if password == password2:
        return
    else:
        raise ValidationError("Passwords do not match.")

class UserRegistration(forms.Form):
    account_name = forms.CharField(widget=forms.TextInput(attrs={'size': '20'}),
                                   validators=[validators.MaxLengthValidator, isValidUsername])
    full_name = forms.CharField(widget=forms.TextInput(attrs={'size': '20'}),
                                validators=[validators.MaxLengthValidator])
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '20'}),
                             validators=[validators.EmailValidator])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                               validators=[validators.MaxLengthValidator])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                                validators=[validators.MaxLengthValidator])

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '20'}),
                             validators=[validators.MaxLengthValidator, existsEmail])

class ResetPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                               validators=[validators.MaxLengthValidator])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                                validators=[validators.MaxLengthValidator])