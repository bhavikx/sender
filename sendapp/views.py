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
	drafts = EmailDraft.objects.all()
	email_list = EmailList.objects.all()	
	
	context = {
		'home' : 'active',
		'drafts' : drafts,
		'email_list' : email_list,
	}
	return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def sendEmailView(request, eid):
	email = EmailDraft.objects.get(id = eid)
	email_list = EmailList.objects.all()

	if request.method == 'POST':
		items = EmailFromList.objects.all()

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
		'email' : email,
		'email_list' : email_list
	}
	
	return render(request, 'send_email.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def EmailFromListView(request):
	form = FromEmailFromListForm()
	item = EmailFromList.objects.all()

	context = {

		'emailsetting' : 'active',
		'form' : form,
		'item' : item
	}

	if request.method == 'POST':
		form = SetEmailToListForm(request.POST)
		item = SetEmailToList.objects.all()

		if form.is_valid():
			form.save()

			context = {
				'form' : form,
				'item' : item
			}
			messages.success(request, 'Email Added To List.')
			return redirect('/set-user/', context)

	return render(request, 'email_settings.html', context)

def defaultEmailView(request, uid):

	item = SetEmailToList.objects.get(id=uid)
	all_item = SetEmailToList.objects.all()
	for i in all_item:
		i.isDefault = False
		i.save()

	item.isDefault = True
	item.save()

	return redirect('set-user')


def unsetDefaultView(request, uid):

	item = SetEmailToList.objects.get(id = uid)

	item.isDefault = False
	item.save()

	return redirect("set-user")


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def editEmailView(request, eid):
	item = SetEmailToList.objects.get(id = eid)
	form = SetEmailToListForm(instance = item)

	if request.method == 'POST':
		form = SetEmailToListForm(request.POST, instance = item)

		if form.is_valid:
			form.save()
			messages.success(request, 'Email Is Updated.')
			return redirect('set-user')

	context = {
		'emailsetting' : 'active',
		'item' : item,
		'form' : form,
	}
	return render(request, 'edit_email.html', context)

def deleteEmailView(request, did):
	item = SetEmailToList.objects.get(id = did)
	item.delete()
	messages.success(request, 'Email Is Deleted.')
	return redirect('set-user')


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def createEmailDraftView(request):
	form = EmailDraftForm()

	if request.method == "POST":
		form = EmailDraftForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'draft added to list.')
			return redirect('home')

	context = {
		'home' : 'active',
		'form' : form
	}
	return render(request, 'email_draft_form.html', context)


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
	form = TempEmailListForm()
	item = TempEmailList.objects.all()

	if request.method == "POST":
		form = TempEmailListForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('second-step')

	context = {
		'home' : 'active',
		'form': form,
		'item' : item
	}
	return render(request, '2new_email_list.html', context)


def deleteEmailListView(request):
	if request.method == "POST":
		form = EmailListForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('second-step')
		else:
			return redirect('first-step')


	item = TempEmailList.objects.all()
	item.delete()

	i = EmailList.objects.all().last()
	i.delete()

	return redirect('home')


def saveEmailListView(request):
	temp_list = TempEmailList.objects.all()
	email_list = EmailList.objects.all().last()

	empty = []
	for email in temp_list:
		empty.append(email.tempEmailList)

	email_list.emailList = empty

	email_list.save()
	temp_list.delete()

	messages.success(request, 'List Added...')
	return redirect('home')

def selectEmailListView(request, sid):
	all_item = EmailList.objects.all()
	item = EmailList.objects.get(id = sid)

	for i in all_item:
		i.selectedEmailList = False
		i.save()

	item.selectedEmailList = True
	item.save()

	return redirect('home')

def unselectEmailListView(request):
	item = EmailList.objects.all()

	for i in item:
		i.selectedEmailList = False
		i.save()

	return redirect('home') 


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def editEmailDraftView(request, eid):
	email = EmailDraft.objects.get(id = eid)
	form = EmailDraftForm(instance = email)

	if request.method == "POST":
		form = EmailDraftForm(request.POST, instance = email)
		if form.is_valid:
			form.save()
			messages.success(request, 'Email Draft Updated')			
			return redirect('home')

	context = {
		'home' : 'active',
		'email' : email,
		'form' : form,
	}
	return render(request, 'edit_email_draft.html', context)

def deleteEmailDraftView(request, eid):
	email = EmailDraft.objects.get(id = eid)

	email.delete()

	messages.success(request, 'Email Draft Deleted')
	return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def editEmailListView(request, did):
	email_edit = EmailList.objects.get(id = did)

	email_list = ast.literal_eval(email_edit.emailList)

	context = {
		'home' : 'active',
		'email_edit' : email_edit,
		'email_list' : email_list,
	}
	return render(request,'edit_email_list.html', context)

def deleteListView(request, did):
	item = EmailList.objects.get(id = did)

	item.delete()

	messages.success(request, item.emailListName + ' List Deleted')

	return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles = ['user', 'admin'])
def deleteEmailListItemView(request, did, index):
	email_edit = EmailList.objects.get(id = did)
	email_list = ast.literal_eval(email_edit.emailList)

	count = 0

	for e in email_list:
		count = count + 1
		if count == index:
			email_list.remove(e)

	email_edit.emailList = email_list
	email_edit.save()

	if len(email_edit.emailList) == 0:
		email_edit.delete()

		messages.success(request, ' List Deleted')
		return redirect('home')

	context = {
		'home' : 'active',
		'email_edit' : email_edit,
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