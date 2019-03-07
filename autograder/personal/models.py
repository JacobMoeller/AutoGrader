from django.db import models
from datetime import timedelta
from django.utils import timezone

# Create your models here.
class Courses(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_title = models.CharField(max_length=30, blank=False, null=False)
    instructor_username = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

def one_month_from_today():
    return timezone.now() + timedelta(days=30)

class Invite(models.Model):
    invite_id = models.IntegerField(primary_key=True)
    sender_username = models.CharField(max_length=20, blank=False, null=False)
    rec_username = models.CharField(max_length=20, blank=True, null=True)
    course_id = models.ForeignKey('Courses', models.DO_NOTHING, blank=False, null=False)
    level_of_invite = models.CharField(max_length=10, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateField(default=one_month_from_today, null=False)

class Assignment(models.Model):
    assignment_id = models.IntegerField(primary_key=True)
    course_id = models.ForeignKey('Courses', models.DO_NOTHING, blank=False, null=False)
    assignment_description = models.CharField(max_length=200, blank=False, null=False)
    optional_notes = models.CharField(max_length=200, blank=True, null=True)
    acceptance_criteria = models.CharField(max_length=200, blank=False, null=False)
    testing_criteria = models.CharField(max_length=200, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_on = models.DateTimeField(auto_now_add=False, null=True) 

class Submission(models.Model):
    submission_id = models.IntegerField(primary_key=True)
    assignment_id = models.ForeignKey('Assignment', models.DO_NOTHING, blank=False, null=False)
    submitted_user = models.CharField(max_length=20, blank=False, null=False)
    submitted_on = models.DateTimeField(auto_now_add=True)
    submission_number = models.IntegerField(default=1)
    submitted_filename = models.CharField(max_length=20, blank=True, null=True) 
