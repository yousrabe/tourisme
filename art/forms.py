# coding=utf-8
from art.models import *
from django import forms
from django.forms import ModelForm


class RegisterForm(ModelForm):
    first_name = forms.CharField(label='Votre prénom', required=True)
    last_name = forms.CharField(label='Votre nom', required=True)
    email = forms.EmailField(label='Votre adresse e-mail', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Votre mot de passe', required=True)
    adress = forms.CharField(label='Votre adress', required=True)
    telephone = forms.CharField(label='Votre telephone', required=True)
    code_post = forms.CharField(label='Votre code postale', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class RegisterFormUpdate(ModelForm):
    first_name = forms.CharField(label='Votre prénom', required=True)
    last_name = forms.CharField(label='Votre nom', required=True)
    email = forms.EmailField(label='Votre adresse e-mail', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class LoginForm(ModelForm):
    username = forms.CharField(label='Votre nom utilisateur', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Votre mot de passe', required=False)

    class Meta:
        model = User
        fields = [ 'username', 'password']

class AddAddress(ModelForm):
    class Meta:
        model = Address
        fields = ['gender', 'first_name', 'last_name', 'company', 'address', 'additional_address',
                  'postcode', 'city', 'phone', 'mobilephone', 'fax', 'workphone']

class IssuesForm(ModelForm):
    name = forms.CharField(label='Votre nom', required=True)
    desc = forms.CharField(label='Description', required=True)

    class Meta:
        model = Issues
        fields = ['name', 'desc']