from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','password1','password2')

    def clean(self):
        cleaned_data = super().clean()
        password1=cleaned_data.get('password1')
        password2=cleaned_data.get('password2')
        if not password1 == password2:
            self.add_error('password2', "Please enter same password")
        return cleaned_data

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