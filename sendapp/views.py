from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .form import *
from .models import *
from .decorators import *
from .email import send

import ast

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@unauthenticated_user
def registerView(request):
	form = RegisterUserForm()

	if request.method == 'POST':
		form = RegisterUserForm(request.POST)

		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'account was created for ' + username)
			return redirect('login')

	context = {
		'form' : form
	}
	return render(request, "register.html", context)

@unauthenticated_user
def loginView(request):

	if request.method == 'POST':
	 	username = request.POST.get('username')
	 	password = request.POST.get('password')
	 	user = authenticate(request, username = username, password = password)

	 	if user is not None:
	 		login(request, user)
	 		return redirect('home')

	 	else:
	 		messages.info(request, "username Or password is incorrect, try again.")

	context = {}
	return render(request, "login.html", context)

def logoutView(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def homeView(request):
	u = UserProfile.objects.get(user = request.user)

	drafts = EmailDraft.objects.filter(user = u)
	email_list = EmailList.objects.filter(user = u)	

	context = {
		'home' : 'active',
		'drafts' : drafts,
		'email_list' : email_list,
	}
	return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def sendEmailView(request, eid):
	u = UserProfile.objects.get(user = request.user)

	email_draft = EmailDraft.objects.get(id = eid)
	email_list = EmailList.objects.filter(user = u)

	if request.method == 'POST':
		email_list = EmailFromList.objects.filter(user = u)

		for e in email_list:
			if e.selectedEmailList == True:
				to_list = e.emailList

		print("to_list")
		print(to_list)
		print(type(to_list))

		to = ast.literal_eval(to_list)
		print(",,,")
		print(type(to))
		print(to)

		for i in items:
			if i.isDefault == True:
				user = i
	
		subject = email.emailDraftSubject
		message = email.emailDraftMessage

		sender = user.userEmail
		password = user.userPassword

		var = sender.split("@")[-1]

		if var == "gmail.com":
			smtpVar = "smtp.gmail.com"

		elif var == "hotmail.com" or "outlook.com":
			smtpVar = "smtp-mail.outlook.com"

		elif var =="yahoo.com":
			smtpVar = "smtp.mail.yahoo.com"
	
		send(to, subject, message, sender, password, smtpVar)

		messages.success(request,'email is sent')
		return redirect('/')

	context = {
		'home' : 'active',
		'email_draft' : email_draft,
		'email_list' : email_list
	}
	
	return render(request, 'send_email.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def createEmailDraftView(request):
	form = EmailDraftForm()

	if request.method == "POST":
		form = EmailDraftForm(request.POST)

		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user.userprofile
			obj.save()

			messages.success(request, 'draft added to list.')
			return redirect('home')

	context = {
		'home' : 'active',
		'form' : form
	}
	return render(request, 'email_draft_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def editEmailDraftView(request, eid):
	email_draft = EmailDraft.objects.get(id = eid)
	form = EmailDraftForm(instance = email_draft)

	if request.method == "POST":
		form = EmailDraftForm(request.POST, instance = email_draft)
		if form.is_valid:
			form.save()
			messages.success(request, 'Email Draft Updated')			
			return redirect('home')

	context = {
		'home' : 'active',
		'email_draft' : email_draft,
		'form' : form,
	}
	return render(request, 'edit_email_draft.html', context)


def deleteEmailDraftView(request, eid):
	email_draft = EmailDraft.objects.get(id = eid)

	email_draft.delete()

	messages.success(request, 'Email Draft Deleted')
	return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def EmailFromListView(request):
	u = UserProfile.objects.get(user = request.user)

	email_from_list = EmailFromList.objects.filter(user = u)
	form = EmailFromListForm()

	if request.method == 'POST':
		form = EmailFromListForm(request.POST)

		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user.userprofile
			obj.save()

			messages.success(request, 'Email Added To List.')
			return redirect('set-user')

	context = {
		'emailsetting' : 'active',
		'form' : form,
		'email_from_list' : email_from_list
	}
	return render(request, 'email_settings.html', context)

def defaultEmailView(request, uid):
	u = UserProfile.objects.get(user = request.user)

	email_from_list = EmailFromList.objects.filter(user = u)
	email_from = EmailFromList.objects.get(id=uid)

	for i in email_from_list:
		print(i)
		print(i.isDefault)
		i.isDefault = False
		i.save()

	email_from.isDefault = True
	email_from.save()

	return redirect('set-user')


def unsetDefaultView(request, uid):
	email_from = SetEmailToList.objects.get(id = uid)

	email_from.isDefault = False
	email_from.save()

	return redirect("set-user")


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def editEmailFromView(request, eid):
	email_from = EmailFromList.objects.get(id = eid)
	form = EmailFromListForm(instance = email_from)

	if request.method == 'POST':
		form = EmailFromListForm(request.POST, instance = email_from)

		if form.is_valid:
			form.save()
			messages.success(request, 'Email Is Updated.')
			return redirect('set-user')

	context = {
		'emailsetting' : 'active',
		'email_from' : email_from,
		'form' : form,
	}
	return render(request, 'edit_email_from.html', context)

def deleteEmailFromView(request, did):
	email_from = EmailFromList.objects.get(id = did)
	email_from.delete()

	messages.success(request, 'Email Is Deleted.')
	return redirect('set-user')



@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def firstStepView(request):
	form = EmailListForm()

	context = {
		'home' : 'active',
		'form' : form
	}
	return render(request, '1new_email_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def secondStepView(request):
	temp_form = TempEmailListForm()
	temp_email_list = TempEmailList.objects.all()

	if request.method == "POST":
		temp_form = TempEmailListForm(request.POST)

		if temp_form.is_valid():
			temp_form.save()
			return redirect('second-step')

	context = {
		'home' : 'active',
		'temp_form': temp_form,
		'temp_email_list' : temp_email_list
	}
	return render(request, '2new_email_list.html', context)


def deleteEmailListView(request):
	#this post is checked from 1stnew_email_list.html bc i was too lazy ro create one
	if request.method == "POST":
		form = EmailListForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user.userprofile
			obj.save()
			return redirect('second-step')
		else:
			return redirect('first-step')


	temp_email_list = TempEmailList.objects.all()
	temp_email_list.delete()

	u = UserProfile.objects.get(user = request.user)

	email_list = EmailList.objects.filter(user = u).last()
	email_list.delete()

	return redirect('home')


def saveEmailListView(request):
	temp_email_list = TempEmailList.objects.all()
	u = UserProfile.objects.get(user = request.user)
	email_list = EmailList.objects.filter(user = u).last()

	empty = []
	for email in temp_email_list:
		empty.append(email.tempEmailList)

	email_list.emailList = empty

	email_list.save()
	temp_email_list.delete()

	messages.success(request, 'List Added...')
	return redirect('home')

def selectEmailListView(request, sid):
	u = UserProfile.objects.get(user = request.user)
	email_list = EmailList.objects.filter(user = u)
	email = EmailList.objects.get(id = sid)

	for email in email_list:
		email.selectedEmailList = False
		email.save()

	email.selectedEmailList = True
	email.save()

	return redirect('home')

def unselectEmailListView(request):
	u = UserProfile.objects.get(user = request.user)
	email_list = EmailList.objects.filter(user = u)

	for email in email_list:
		email.selectedEmailList = False
		email.save()

	return redirect('home') 


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def editEmailListView(request, did):
	edit_email_list = EmailList.objects.get(id = did)

	email_list = ast.literal_eval(edit_email_list.emailList)

	context = {
		'home' : 'active',
		'edit_email_list' : edit_email_list,
		'email_list' : email_list,
	}
	return render(request,'edit_email_list.html', context)

def deleteListView(request, did):
	email = EmailList.objects.get(id = did)

	email.delete()

	messages.success(request, email.emailListName + ' List Deleted')

	return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def deleteEmailListItemView(request, did, index):
	edit_email_list = EmailList.objects.get(id = did)
	email_list = ast.literal_eval(edit_email_list.emailList)

	count = 0

	for e in email_list:
		count = count + 1
		if count == index:
			email_list.remove(e)

	edit_email_list.emailList = email_list
	edit_email_list.save()

	if len(edit_email_list.emailList) == 0:
		edit_email_list.delete()

		messages.success(request, ' List Deleted')
		return redirect('home')

	context = {
		'home' : 'active',
		'edit_email_list' : edit_email_list,
		'email_list' : email_list
	}

	return render(request, "edit_email_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def addToCurrlistView(request, eid):
	form = TempEmailListForm()
	email_list = EmailList.objects.get(id = eid)

	temp = TempEmailList.objects.all()
	le = len(temp)
	temp = reversed(temp)

	items = ast.literal_eval(email_list.emailList)
	email_items = reversed(items)

	if request.method == 'POST':
		form = TempEmailListForm(request.POST)

		if form.is_valid:
			form.save()
			return redirect('add-to-currlist', eid)

	context = {
		'home' : 'active',
		'form' : form,
		'email_list' : email_list,
		'email_items' : email_items,
		'temp' : temp,
		'le' : le
		}
	return render(request, 'add_to_currlist.html', context)

def saveEditedEmailListView(request, eid):
	temp_list = TempEmailList.objects.all()
	email_list = EmailList.objects.get(id = eid)

	empty = ast.literal_eval(email_list.emailList)

	for email in temp_list:
		empty.append(email.tempEmailList)

	email_list.emailList =  empty

	email_list.save()
	temp_list.delete()

	messages.success(request, 'List Added...')
	return redirect('edit-email-list', eid)


def deleteEditedEmailListView(request, eid):
	delete_item = TempEmailList.objects.all()
	delete_item.delete()

	return redirect('edit-email-list', eid)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def editEmailItemView(request, eid, index):
	email_edit = EmailList.objects.get(id=eid)
	email_list = ast.literal_eval(email_edit.emailList)

	count = 0

	item = ""

	for i in email_list:
		count = count + 1
		if count == index:
			item = i

	temp_email = TempEmailList.objects.create(tempEmailList = item)

	form = TempEmailListForm(instance = temp_email)

	if request.method == "POST":
		form = TempEmailListForm(request.POST, instance = temp_email)

		if form.is_valid:
			form.save()

			for i in range(len(email_list)):
				print(i)
				print(index)
				if i == index-1:
					print(temp_email.tempEmailList)
					email_list[i] = temp_email.tempEmailList
					print(email_list[i])

			email_edit.emailList = email_list
			email_edit.save()

			print("-")
			print(email_list)
			print("..")
			print(email_edit.emailList)

			TempEmailList.objects.all().delete()

			return redirect('edit-email-list', email_edit.id)


	temp_email.delete()
	context = {
		'home' : 'active',
		'form' : form,
		'eid' : eid,
	}
	return render(request, "edit_email_item.html", context)


'''
		temp = []
		for i in email_list:
			temp.append(i.emailList)

		temp = [i.replace('"', "").strip('[]').split(', ') for i in temp]

		print(type(temp))
		print(temp)
		for t in temp:
			for i in range(len(t)):
				t[i] = t[i].strip("'")

		print("temp")
		print(type(temp))
		print(temp)
'''