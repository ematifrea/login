from django import forms


class UserRegistration(forms.Form):
    account_name = forms.CharField(max_length=100, required=True)
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(max_length=50, required=True)
    password2 = forms.CharField(max_length=50, required=True)





