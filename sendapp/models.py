from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(to=User, on_delete = models.CASCADE, null=True, blank=True)

	name = models.CharField(max_length = 30, blank = False)
	def __str__(self):
		return "%s" % self.user	

class EmailFromList(models.Model):
	user = models.ForeignKey(to=UserProfile, on_delete = models.CASCADE, null=True, blank=True)

	userEmail = models.EmailField(max_length = 200, blank = False, null = True)
	userPassword = models.CharField(max_length = 32, blank = False, null = True)
	isDefault = models.BooleanField(default = False)

	def __str__(self):
		return self.userEmail

class EmailDraft(models.Model):
	user = models.ForeignKey(to=UserProfile, on_delete = models.CASCADE, null=True, blank=True)

	emailDraftSubject = models.CharField(max_length = 40, blank = False, null = True)
	emailDraftMessage = models.TextField(max_length = 300, blank = False, null = True)
	timeDraftCreated = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.emailDraftSubject
	
class EmailList(models.Model):
	user = models.ForeignKey(to=UserProfile, on_delete = models.CASCADE, null=True, blank=True)

	emailListName = models.CharField(max_length = 20, blank = False, null = True)
	emailList = models.CharField(max_length = 2500, blank = False, null = True)
	selectedEmailList = models.BooleanField(default = False)

	def __str__(self):
		return self.emailListName

class TempEmailList(models.Model):
	tempEmailList = models.EmailField(max_length = 200)

	def __str__(self):
		return self.tempEmailList