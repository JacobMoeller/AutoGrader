from django.db import models
from datetime import timedelta, date
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Courses(models.Model):
    course_crn = models.IntegerField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="CRN",
        validators=[MinValueValidator(1)])
    course_title = models.CharField(max_length=50, blank=False, null=False)
    course_number = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1)])
    instructor_username = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'groups__name': "Instructor"},
        blank=False,
        null=False,
        to_field='username')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course"
        ordering = ['course_number', ]

    def __str__(self):
        return f'{self.course_number} {self.course_title} ({self.course_crn})'

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.id})


def one_month_from_today():
    return timezone.now() + timedelta(days=30)


class Invite(models.Model):
    sender_username = models.ForeignKey(
            User,
            on_delete=models.DO_NOTHING,
            limit_choices_to={'groups__name': "Instructor"},
            blank=False,
            null=False,
            to_field='username',
            related_name='sender',
            verbose_name='from')
    rec_username = models.ForeignKey(
            User,
            on_delete=models.DO_NOTHING,
            blank=False,
            null=False,
            to_field='username',
            related_name='receiver',
            verbose_name='to')
    course_id = models.ForeignKey(
        'Courses', on_delete=models.CASCADE, blank=False, null=False)
    INVITE_TYPES = (
        ('g', 'Grader'),
        ('s', 'Student'),
        ('i', 'Instructor'),
    )
    level_of_invite = models.CharField(
        max_length=1, choices=INVITE_TYPES, default='s')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateField(default=one_month_from_today, null=False)

    def time_left(self):
        remaining = self.expires_on - date.today()
        return f'{remaining.days} day(s)'

    class Meta:
        ordering = ['-expires_on', 'sender_username', ]

    def __str__(self):
        return f'{self.get_level_of_invite_display()} Invite for {self.rec_username} ({self.course_id})'


class Assignment(models.Model):
    course_id = models.ForeignKey(
        'Courses', on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=200)
    assignment_description = models.CharField(
        max_length=200, blank=False, null=False)
    optional_notes = models.CharField(max_length=200, blank=True, null=True)
    acceptance_criteria = models.CharField(
        max_length=200, blank=True, null=True)
    testing_criteria = models.CharField(
        max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_on = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        ordering = ['course_id', 'due_on', 'title', ]

    def __str__(self):
        return f'{self.title} (for {self.course_id.course_title})'


class Submission(models.Model):
    assignment_id = models.ForeignKey(
        'Assignment', models.DO_NOTHING, blank=False, null=False)
    submitted_user = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': "Student"},
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING,
        to_field='username')
    submitted_on = models.DateTimeField(auto_now_add=True)
    submission_number = models.IntegerField(default=1)
    submitted_filename = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['submitted_user', 'assignment_id', 'submitted_on', ]

    def __str__(self):
        return f'{self.submitted_user.username}: \
        {self.assignment_id} -- Attempt: {self.submission_number}'


class Takes(models.Model):
    course_id = models.ForeignKey(
        'Courses', models.DO_NOTHING, blank=False, null=False)
    student_username = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': "Student"},
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING,
        to_field='username')
    is_grader_in_course = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name_plural = "Takes"
        ordering = ['course_id__course_number', ]

    def __str__(self):
        takes_record = f'CIS{self.course_id.course_number} - {self.student_username}'
        if(self.is_grader_in_course):
            takes_record += '(Grader)'
        return takes_record
