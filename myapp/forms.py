from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('username', 'first_name', 'last_name', 'email', 'mobile', 'address')

    username=forms.CharField(
        label=('Enter username'),
        widget=forms.TextInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    first_name=forms.CharField(
        label=('Enter First Name'),
        widget=forms.TextInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    last_name=forms.CharField(
        label=('Enter Last Name'),
        widget=forms.TextInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    email=forms.CharField(
        label=('Enter Email Address'),
        widget=forms.EmailInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    mobile=forms.CharField(
        label=('Enter Contact Number'),
        widget=forms.TextInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    address=forms.CharField(
        label=('Enter Address'),
        widget=forms.Textarea(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    password1=forms.CharField(
        label=('Enter Password'),
        widget=forms.PasswordInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    password2=forms.CharField(
        label=('Enter Confirm Password'),
        widget=forms.PasswordInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    

class LoginForm(AuthenticationForm):
    username=forms.CharField(
        label=('Enter username'),
        widget=forms.TextInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )
    password=forms.CharField(
        label=('Enter password'),
        widget=forms.PasswordInput(attrs={'class':'w-100 form-control border-0 py-3 mb-4'})
    )