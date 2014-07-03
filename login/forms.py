from django import forms


class UserRegistration(forms.Form):
    account_name = forms.CharField(max_length=100)
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)


