from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','password1','password2')

    def clean(self):
        password1=self.cleaned_date['password1']
        password2=self.cleaned_date['password2']
        if username:
            if username.length 

class UserLoginForm(forms.ModelForm):
    password=forms.CharField(label="password", widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username', 'password')

    def clean(self):
        if self.is_valid():
            username=self.cleaned_data['username']
            password=self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid credentials")