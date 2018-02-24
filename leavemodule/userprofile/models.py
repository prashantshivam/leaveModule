# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class FacultyProfile(models.Model):
	designation = (
			('driver', 'driver'),
			('executiveEngineer', 'Executive Enginerr'),
			('js', 'junior Superitendent'),
			('sa', 'senior assistant'),
			('ja', 'junior assistant'),
			('st', 'senior techinician'),
			('driver', 'driver'),
			('jt', 'junior technician'),
			('ar', 'assistant registrar'),
			('ja', 'junior assistant'),
			('dr', 'deputy registrar'),
			('Professor', 'Professor'),
			('Associate Professor', 'Associate Professor'),
			('Assistant Professor', 'Assistant Professor'),
			('Research Engineer', 'Research Engineer'),
		)
	department = (
			('cse', 'cse'),
			('ece', 'ece'),
			('studentaffairs', 'studdent affairs'),
			('ga', 'General Administartion'),
			('cc', 'computer center'),
			('workshop', 'workshop'),
			('security', 'security'),
			('ro', 'registrar office'),
			('faga', 'f&a g&a'),
			('purchase', 'store'),
			('fa', 'finance and accounts'),
			('et', 'establishment'),
			('academics', 'academics'),
			('ece', 'ece'),
			('academics', 'academics'),
			('ns', 'natural science'),
			('mechatronics', 'mechatronics'),
			('pc', 'placement cell'),
			('iwd', 'iwd'),
			('otd', 'office of the dean'),
			('directorate', 'directorate'),
			('library', 'library'),
			('ME', 'Mechanical Engineering'),
			('CSE', 'Computer Science and Engineering'),
			('ECE', 'Electronics and communication Engineering'),
			('NS', 'Natural Science'),
			('Design', 'Design'),
		)
	designation1 = (
			('driver', 'driver'),
			('executiveEngineer', 'Executive Enginerr'),
			('js', 'junior Superitendent'),
			('sa', 'senior assistant'),
			('ja', 'junior assistant'),
			('st', 'senior techinician'),
			('driver', 'driver'),
			('jt', 'junior technician'),
			('ar', 'assistant registrar'),
			('ja', 'junior assistant'),
			('dr', 'deputy registrar'),
			('Professor', 'Professor'),
			('Associate Professor', 'Associate Professor'),
			('Assistant Professor', 'Assistant Professor'),
			('Research Engineer', 'Research Engineer'),
			('deanRSPC', 'dean RSPC'),
			('hodme', 'hod ME'),
			('hodcse', 'hod CSE'),
			('headns', 'head NS'),
			('deanacad', 'dean academics'),
			('deanstudents', 'dean students'),
			('director', 'director'),
		)
	leave_authority = (
			('registrar', 'registrar'),
			('deanacad', 'dean academics'),
			('ccc', 'cordinator computer center'),
			('hodece', 'hod ECE'),
			('hodcse', 'hod CSE'),
			('hodme', 'hod ME'),
			('dean', 'dean'),
			('iw', 'incharge workshop'),
			('head', 'head'),
			('director', 'director'),
		)
	staff_faculty = (
			('staff', 'staff'),
			('faculty', 'faculty'),
		)
	user = models.OneToOneField(User, on_delete=models.CASCADE);
	facultyDepartment = models.CharField(max_length=100, choices=department);
	facultyLeaveHead = models.CharField(max_length=100, choices=leave_authority);
	facultyPostForLeave = models.CharField(max_length=100, choices=leave_authority, blank=True, null=True)
	facultyDesignation = models.CharField(max_length=100, choices=designation1, null=True, blank=True)
	facultyPost = models.CharField(max_length=100, choices=designation, null=True)
	pfnumber = models.IntegerField(null=True)
	staff_or_faculty = models.CharField(max_length=100, choices=staff_faculty, null=True);

	def __str__(self):
		return self.user.username

'''
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = FacultyProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)
'''

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FacultyProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.facultyprofile.save()
