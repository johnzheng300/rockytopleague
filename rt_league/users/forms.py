from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2' ]

# updates username and email
class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email',]

# updates profile pic
class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile 
		fields = ['image']