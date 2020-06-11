from django.db import models
from django.contrib.auth.models import User

class UserPro(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)

	name = models.CharField(max_length = 30, blank = False)
	def __str__(self):
		return self.name	

class EmailFromList(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	userEmail = models.EmailField(max_length = 200, blank = False)
	userPassword = models.CharField(max_length = 32, blank = False)
	isDefault = models.BooleanField(default = False)

	def __str__(self):
		return self.userEmail

class EmailDraft(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	emailDraftSubject = models.CharField(max_length = 40, blank = False)
	emailDraftMessage = models.TextField(max_length = 300, blank = False)
	timeDraftCreated = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.emailDraftSubject
	
class EmailList(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	emailListName = models.CharField(max_length = 20, blank = False)
	emailList = models.CharField(max_length = 2500, blank = False)
	selectedEmailList = models.BooleanField(default = False)

	def __str__(self):
		return self.emailListName

class TempEmailList(models.Model):
	tempEmailList = models.EmailField(max_length = 200)

	def __str__(self):
		return self.tempEmailList