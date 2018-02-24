# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect;
from django.http import HttpResponse;
from django.contrib.auth.decorators import login_required;
from . forms import UserForm, FacultyProfileForm, SignUpForm;
from django.contrib.auth.models import User;
from django.db import transaction
from . models import FacultyProfile
from leavemodule.models import Leave
import os;
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from leavemodule.models import Leave, ApplicationRequest, RemainingLeaves
from django.shortcuts import get_object_or_404


# Create your views here.
 
#Test My work
def test(request):
	leaveuser = Leave.objects.all().filter(user=request.user);
	facultyuser = FacultyProfile.objects.all().filter(user=request.user)
	print(facultyuser)
	print(leaveuser);
	return HttpResponse('Check it')



#Signup Form 
def signup(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
	if request.method=='POST':
	    form = SignUpForm(request.POST);
	    if form.is_valid():
	    	form.save();
	    	username = form.cleaned_data.get('username');
	    	raw_password = form.cleaned_data.get('password');
	    	user = authenticate(username=username, password=raw_password);
	    	login(request, user);
	    	return HttpResponse('Created');
	else:
	    form = SignUpForm();
	return render(request, BASE_DIR+'/templates/pages/signup.html', {'form':form});

@login_required(login_url='/login')
@transaction.atomic
def update_faculty_profile(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));	

	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user);
		faculty_form = FacultyProfileForm(request.POST, instance=request.user.facultyprofile)

		if user_form.is_valid() and faculty_form.is_valid():
			user_form.save();
			faculty_form.save();
			return HttpResponse("Thanks");
		
	else:
		user_form = UserForm(instance=request.user);
		faculty_form = FacultyProfileForm(instance=request.user.facultyprofile);

	return render(request, BASE_DIR + '/templates/pages/signup.html', {
			'user_form':user_form,
			'faculty_form': faculty_form
		})

#function to call user homepage
def user_home(request):
	return HttpResponse("Home Page")

@login_required(login_url='/login')
def leaveDetails(request, username):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
	if username == request.user.username:
		user = get_object_or_404(User, username=username);
		leave = Leave.objects.filter(user=request.user);
		leaveDetails = RemainingLeaves.objects.filter(user = request.user).first();
		print(leaveDetails);
		return render(request, BASE_DIR+ '/templates/pages/leaveDetails.html', {'user': user,'leave': leave, 'details': leaveDetails});
	else:
		return HttpResponse('You have no rights to access this page');

# Function to call user profile page	
@login_required(login_url='/login')
def profile(request):
 	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
 	user = get_object_or_404(User, username=request.user.username);
 	leave = Leave.objects.filter(user=request.user);
 	faculty = FacultyProfile.objects.filter(user=request.user).first();
 	remainingLeave = RemainingLeaves.objects.filter(user = request.user).first();
 	#print(remainingLeave)
 	print(faculty.facultyPostForLeave)
 	leaveRequest = [];	
 	if faculty.facultyPostForLeave is not None:
 		leaveRequest.append(Leave.objects.filter(leaveto=faculty.facultyPostForLeave, processing_status='processing'));
 	try:
		leaveRequestLength = len(leaveRequest[0]);
	except:
		leaveRequestLength = 0;
	print(leaveRequest)
	# 	print(headLeave);
 	return render(request, BASE_DIR+ '/templates/pages/profile.html', {'user': user, 'length': leaveRequestLength, 'leave': leave, 'count': len(leave), 'faculty': faculty, 'leaveRequest': leaveRequest, 'remainingLeave': remainingLeave});

@login_required(login_url='/login')
def approve(request, username):
	if username == request.user.username:
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
		user = get_object_or_404(User, username=username);
		leave = Leave.objects.filter(user=request.user);
		faculty = FacultyProfile.objects.filter(user=request.user).first();
		remainingLeave = RemainingLeaves.objects.filter(user = request.user).first();

		leaveRequest = [];
		if faculty.facultyPostForLeave is not None:
			leaveRequest.append(Leave.objects.filter(leaveto=faculty.facultyPostForLeave, processing_status='processing'));
		try:
			leaveRequestLength = len(leaveRequest[0]);
		except:
			leaveRequestLength = 0;
		
		print(leaveRequest)
		return render(request, BASE_DIR + '/templates/pages/approve.html', {'user': user, 'length': leaveRequestLength, 'leave': leave, 'count': len(leave), 'faculty': faculty, 'leaveRequest': leaveRequest, 'remainingLeave': remainingLeave});			
	return HttpResponse("You have no rights to access this page");

@login_required(login_url='/login')
def leaveShow(request, username, leave_id):
	if username == request.user.username:
		print(leave_id);
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
		user = get_object_or_404(User, username=username);
		leaveData = Leave.objects.filter(leave_id = leave_id).first();
		print(leaveData)
		return render(request, BASE_DIR + '/templates/pages/leave_data.html', {'user': user, 'leaveData': leaveData});
	return HttpResponse("You are not allowed to visit this page");
		
@login_required(login_url='/login')
def accept(request, username, leave_id):
	#if username == request.user.username:
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
		user = get_object_or_404(User, username=username);
		leaveData = Leave.objects.filter(leave_id=leave_id).first();
		leaveData.processing_status = 'accepted';
		userval = leaveData.user;
		leave_type = leaveData.leave_type;
		leave_days = (leaveData.end_date - leaveData.start_date).days+1;
	
		remainingLeave = RemainingLeaves.objects.only(leave_type).filter(user=userval).first();
		if leave_type == 'casual':
			print('yes')
			remainingLeave.casual = remainingLeave.casual - leave_days;
		elif leave_type  == 'vacation':
			remainingLeave.vacation = remainingLeave.vacation - leaveDays;
		elif leave_type == 'commuted':
			remainingLeave.commuted = remainingLeave.commuted - leaveDays;
		elif leave_type == 'special_casual':
			remainingLeave.special_casual = remainingLeave.special_casual - leaveDays;
		elif leave_type == 'restricted':
			remainingLeave.restricted = remainingLeave.restricted - leaveDays;

		remainingLeave.save();
		leaveData.save();
		# user = get_object_or_404(User, username=username);
		return HttpResponseRedirect('/profile');
	#return HttpResponse("You have no rights to access this page");
@login_required(login_url='/login')
def delete(request, username, leave_id):
	#if username == request.user.username:
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
		user = get_object_or_404(User, username=username);
		leaveData = Leave.objects.filter(leave_id=leave_id).first();
		leaveData.processing_status = 'rejected';
		leaveData.save();
		return HttpResponseRedirect('/profile');

@login_required(login_url='/login')
def forward(request, username, leave_id):
	user = get_object_or_404(User, username=username);

	faculty = Leave.objects.filter(user = user, leave_id = leave_id).first();
	faculty.leaveto = 'director';
	print(faculty.leaveto)
	faculty.save();
	return HttpResponseRedirect('/profile/'+request.user.username + '/Approve');
	
