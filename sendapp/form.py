from django.forms import ModelForm
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class EmailFromListForm(ModelForm):
	class Meta:
		model = EmailFromList
		fields = '__all__'
		exclude = ['user']
		widgets = {
      		'userPassword': forms.PasswordInput()
         }
		

class EmailDraftForm(ModelForm):
	class Meta:
		model = EmailDraft
		fields = '__all__'
		exclude = ['timeDraftCreated', 'user']
		
class TempEmailListForm(ModelForm):
	class Meta:
		model = TempEmailList
		fields = '__all__'
		exclude = ['user']

class EmailListForm(ModelForm):
	class Meta:
		model = EmailList
		fields = ['emailListName']
		exclude = ['user']

class RegisterUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']