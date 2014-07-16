from crispy_forms.bootstrap import FormActions
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from login.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


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


class UserRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['account_name', 'full_name', 'email', 'password']

    password = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                               validators=[validators.MaxLengthValidator])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                                validators=[validators.MaxLengthValidator])

    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['password2'].label = "Re-enter password"
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login:register'

        self.helper.layout = Layout(
            Field('account_name', placeholder="Account name", css_class='input-xlarge'),
            Field('full_name', placeholder="Full name", css_class='input-xlarge'),
            Field('email', placeholder="email", css_class='input-xlarge'),
            Field('password', placeholder="Password", css_class='input-xlarge'),
            Field('password2', placeholder="Re-enter password", css_class='input-xlarge'),
            FormActions(Submit('register', 'Register', css_class="btn-primary")),
        )


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '20'}),
                             validators=[validators.MaxLengthValidator, existsEmail])


class ResetPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                               validators=[validators.MaxLengthValidator])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                                validators=[validators.MaxLengthValidator])


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['account_name', 'password']

    password = forms.CharField(widget=forms.PasswordInput(attrs={'size': '20'}),
                               validators=[validators.MaxLengthValidator])

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login:login'

        self.helper.layout = Layout(
            Field('account_name', placeholder="Account name", css_class='input-xlarge'),
            Field('password', placeholder="Password", css_class='input-xlarge'),
            FormActions(Submit('login', 'Login', css_class="btn-primary btn-lg active")),
        )