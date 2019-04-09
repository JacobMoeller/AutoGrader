from django.db import models
from datetime import timedelta, date
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

# used to establish user foreign keys in models
User = get_user_model()


class TakingMixin(models.Model):
    # different levels of invite
    GROUP_LEVELS = (
        ('g', 'Grader'),
        ('s', 'Student'),
        ('i', 'Instructor'),
    )

    # reference to the course the user is being invited to
    course_id = models.ForeignKey(
        'Courses', on_delete=models.CASCADE, blank=False, null=False)
    user_level = models.CharField(
        max_length=1, choices=GROUP_LEVELS, default='s')

    class Meta:
        abstract = True

# Model for courses
class Courses(models.Model):
    # Unique crn for course; cannot be blank/null
    course_crn = models.IntegerField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="CRN",
        validators=[MinValueValidator(1)])
    # Title for course; Ex: Software Engineering
    course_title = models.CharField(max_length=50, blank=False, null=False)
    # Number for course Ex: 201, 420
    course_number = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1)])
    # Username for the instructor of the course; references user in user table
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

    # defines how the object will be specified as a string
    def __str__(self):
        return f'{self.course_number} {self.course_title} ({self.course_crn})'

    def get_absolute_url(self):
       return reverse('course_detail', kwargs={'pk': self.id})

# used to add expiration date
def one_month_from_today():
    return timezone.now() + timedelta(days=30)


# Model for invites
class Invite(TakingMixin):
    # Username for the instructor of the course the invite references
    sender_username = models.ForeignKey(
            User,
            on_delete=models.DO_NOTHING,
            limit_choices_to={'groups__name': "Instructor"},
            blank=False,
            null=False,
            to_field='username',
            related_name='sender',
            verbose_name='from')
    # Username for the student/grader/instructor being invited; references user in user table
    rec_username = models.ForeignKey(
            User,
            on_delete=models.DO_NOTHING,
            blank=False,
            null=False,
            to_field='username',
            related_name='receiver',
            verbose_name='to')
    # specifies an invite will expire in one month
    expires_on = models.DateField(default=one_month_from_today, null=False)
    # timestamp for when the invite was created
    created_at = models.DateTimeField(auto_now_add=True)

    #   determines time left until expiration
    def time_left(self):
        remaining = self.expires_on - date.today()
        return f'{remaining.days} day(s)'

    class Meta:
        ordering = ['-expires_on', 'sender_username', ]

    # defines how the object will be specified as a string
    def __str__(self):
        return f'{self.get_user_level_display()} \
            Invite for {self.rec_username} ({self.course_id})'


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


# Model for Submissions
class Submission(models.Model):
    # Reference to the assignment the submission corresponds to
    assignment_id = models.ForeignKey(
        'Assignment', models.DO_NOTHING, blank=False, null=False)
    # user that entered submission
    submitted_user = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': "Student"},
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING,
        to_field='username')
    # timestamp for when the assignment was submitted
    submitted_on = models.DateTimeField(auto_now_add=True)
    # current submission number
    submission_number = models.IntegerField(default=1)
    # name of the submitted file
    submitted_filename = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['submitted_user', 'assignment_id', 'submitted_on', ]
        # defines how the object will be specified as a string
    def __str__(self):
        return f'{self.submitted_user.username}: \
        {self.assignment_id} -- Attempt: {self.submission_number}'


# Relationship model for which course is taken by a student/grader/instructor
class Takes(TakingMixin):
    # username of the student taking the course
    username = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING,
        to_field='username')

    class Meta:
        verbose_name_plural = "Takes"
        ordering = ['course_id__course_number', ]
    # defines how the object will be specified as a string
    def __str__(self):
        takes_record = f'CIS{self.course_id.course_number} \
            - {self.username} ({self.get_user_level_display()})'
        return takes_record
