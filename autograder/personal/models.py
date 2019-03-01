from django.db import models

# Create your models here.
class Courses(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_title = models.CharField(max_length=30, blank=True, null=True)
    instructor_username = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Invite(models.Model):
    invite_id = models.IntegerField(primary_key=True)
    sender_username = models.CharField(max_length=20, blank=True, null=True)
    rec_username = models.CharField(max_length=20, blank=True, null=True)
    course_id = models.ForeignKey('Courses', models.DO_NOTHING, blank=True, null=True)
    level_of_invite = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateField(auto_now=False, auto_now_add=False, null=True)

class Assignment(models.Model):
    assignment_id = models.IntegerField(primary_key=True)
    course_id = models.ForeignKey('Courses', models.DO_NOTHING, blank=True, null=True)
    assignment_description = models.CharField(max_length=200, blank=True, null=True)
    optional_notes = models.CharField(max_length=200, blank=True, null=True)
    acceptance_criteria = models.CharField(max_length=200, blank=True, null=True)
    testing_criteria = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_on = models.DateTimeField(auto_now_add=False, null=True) 

class Submission(models.Model):
    submission_id = models.IntegerField(primary_key=True)
    assignment_id = models.ForeignKey('Assignment', models.DO_NOTHING, blank=True, null=True)
    submitted_user = models.CharField(max_length=20, blank=True, null=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    submission_number = models.IntegerField(null=True)
    submitted_filename = models.CharField(max_length=20, blank=True, null=True) 
