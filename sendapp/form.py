from django.forms import ModelForm
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from crispy_forms.helper import FormHelper

class EmailFromListForm(ModelForm):
	class Meta:
		model = EmailFromList
		fields = '__all__'
		exclude = ['user']
		widgets = {
      		'userPassword': forms.PasswordInput()
        }


	def __init__(self, *args, **kwargs):
		super(EmailFromListForm, self).__init__(*args, **kwargs)
		self.fields['userEmail'].widget.attrs['placeholder'] = 'Email'
		self.fields['userPassword'].widget.attrs['placeholder'] = 'Password'
    	
		self.fields['userEmail'].label = ''
		self.fields['userPassword'].label = ''
		

class EmailDraftForm(ModelForm):
	class Meta:
		model = EmailDraft
		fields = ['emailDraftSubject', 'emailDraftMessage']

	def __init__(self, *args, **kwargs): 
	    super(EmailDraftForm, self).__init__(*args, **kwargs)

	    self.fields['emailDraftSubject'].widget.attrs['placeholder'] = 'Subject'
	    self.fields['emailDraftMessage'].widget.attrs['placeholder'] = 'Message'

	    self.fields['emailDraftSubject'].label = ''
	    self.fields['emailDraftMessage'].label = ''

class EmailListForm(ModelForm):
	class Meta:
		model = EmailList
		fields = ['emailListName']
		exclude = ['user']

	def __init__(self, *args, **kwargs): 
	    super(EmailListForm, self).__init__(*args, **kwargs)

	    self.fields['emailListName'].widget.attrs['placeholder'] = 'Enter List Name'

	    self.fields['emailListName'].label = ''

class RegisterUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


	def __init__(self, *args, **kwargs):
	    super(RegisterUserForm, self).__init__(*args, **kwargs)

	    self.fields['username'].widget.attrs['placeholder'] = 'username'
	    self.fields['email'].widget.attrs['placeholder'] = 'email'
	    self.fields['password1'].widget.attrs['placeholder'] = 'password'
	    self.fields['password2'].widget.attrs['placeholder'] = 're-enter password'

	    self.helper = FormHelper()
	    self.helper.form_show_labels = False

	    for fieldname in ['username', 'email', 'password1', 'password2']:
	    	self.fields[fieldname].help_text = None

class TempEmailListForm(ModelForm):
	class Meta:
		model = TempEmailList
		fields = ['tempEmailList']

	def __init__(self, *args, **kwargs): 
		super(TempEmailListForm, self).__init__(*args, **kwargs)
		
		self.fields['tempEmailList'].widget.attrs['placeholder'] = 'Enter Email'
		self.fields['tempEmailList'].label = ''