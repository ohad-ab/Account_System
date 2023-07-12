from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
# from users.models import User


class SignupForm(UserCreationForm):
    
    email = forms.EmailField

    
    class Meta:
        model = User
        fields = ['username','email']

class LoginForm(forms.ModelForm):

    user_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    
    class Meta:
        model = User
        fields = ['user_name', 'password']

class UpdateForm(forms.ModelForm):
    
    bio = forms.CharField(max_length=500, widget=forms.Textarea)
    location = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['bio', 'location',]