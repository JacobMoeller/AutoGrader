from personal.models import Invite, Courses, Takes
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from personal.forms import InviteForm
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.core.mail import send_mail


# User homepage
# Parameter: request for template render
# Returns: render of homepage, which contains course and invite list
@login_required()
def index(request):
    ''' Dashboard/homepage view. Returns context-based list view of courses
    and invites based on the current user.
    '''
    args = {}
    course_list = None
    invite_list = None
    # Checks to see if user is logged in
    if request.user.is_authenticated:
        # If post is recieved, this means an invite has been accepted
        if request.method == "POST":
            # id for accepted invite
            invite_id = request.POST.get('invite_name')
            # Gets invite based in invite id
            invite = Invite.objects.get(id=invite_id)
            # Places user into course specified in invite model
            Takes.objects.create(
                username=request.user,
                course_id=Courses.objects.get(id=invite.course_id.id),
                user_level=invite.user_level)
            # Removes invite instance, so it cannot be accepted multiple times
            Invite.objects.filter(id=invite_id).delete()

        # gets username for current user
        username = request.user.get_username()
        # gets current list of invites for user
        invite_list = Invite.objects.filter(rec_username=username)
        take_list = Takes.objects.filter(username=username).\
            values_list('course_id', flat=True)
        course_list = Courses.objects.filter(instructor_username=username)

        course_list = course_list | Courses.objects.filter(id__in=take_list)
    args = {'course_list': course_list, 'invite_list': invite_list}
    return render(request, 'personal/homepage.html', args)


# Contact page
# Parameter: request for template render
# Returns: render of contact page
def contact(request):
    return render(
        request, 'personal/basic.html',
        {'content':
            ['If you would like to contact me, please email me.',
                'moellej200@potsdam.edu']})

# COURSES #####################################################################


class CoursesCreate(CreateView):
    ''' A view for creating a course. Uses a generic form base, does not
    include instructor_username or created_at, which are automatically
    populated based on current user and timestamp. Redirects to detail view.
    '''

    model = Courses
    fields = ['course_number', 'course_title', 'course_crn', ]
    template_name = "personal/generic_form.html"

    def form_valid(self, form):
        course = form.save(commit=False)
        course.instructor_username = self.request.user
        if(form.is_valid()):
            if(course.id):
                return HttpResponseRedirect(reverse(
                    'course_detail', kwargs={'pk': course.id}))
        return super(CoursesCreate, self).form_valid(form)


class CoursesUpdate(UpdateView):
    ''' A generic view for updating a course. Throws a permission denied if the
    user tries to modify a course for which they are not an instructor. '''
    model = Courses
    fields = ['course_number', 'course_title', 'course_crn', ]
    template_name = "personal/generic_form.html"
    success_url = reverse_lazy('homepage')

    def get_object(self, *args, **kwargs):
        course = super(CoursesUpdate, self).get_object(*args, **kwargs)
        if course.instructor_username != self.request.user:
            raise PermissionDenied("You don't have permission \
                to edit this course.")
        return course


class CoursesDelete(DeleteView):
    ''' Deletes a course, forces confirmation of delete. Throws error for users
    who try to delete a course for which they are not the instructor.
    '''
    model = Courses
    template_name = "personal/confirm_delete.html"
    success_url = reverse_lazy('homepage')

    def get_object(self, *args, **kwargs):
        course = super(CoursesDelete, self).get_object(*args, **kwargs)
        if course.instructor_username != self.request.user:
            raise PermissionDenied("You don't have permission \
                to delete this course.")
        return course


@login_required()
def create_invite(request, pk):
    ''' Creates invite for a given course id. Only the current instructor can
    generate an invite for a course.
    '''
    course = get_object_or_404(Courses, pk=pk)
    if course.instructor_username != request.user:
        raise PermissionDenied("You don't have permission \
            to create an invite for this course.")

    # Handle GET requests, pass to the form the current user and course objs.
    if request.method == 'GET':
        form = InviteForm(
            sender_username=request.user,
            course_id=course)

    # Handles POST requests; saves POSTed data and redirects to course detail.
    if request.method == 'POST':
        form = InviteForm(
            sender_username=request.user,
            course_id=course,
            data=request.POST)
        if form.is_valid():
            try:
                Takes.objects.get(
                    username=form.data['rec_username'],
                    course_id=form.course_id,
                    user_level=form.data['user_level'],
                )
                raise PermissionDenied("User is already in course.")
            except Takes.DoesNotExist:
                pass
            try:
                Invite.objects.get(
                    rec_username=form.data['rec_username'],
                    course_id=form.course_id,
                    user_level=form.data['user_level'],
                    )
                raise PermissionDenied("Invite already exists for this user \
                    and course.")
            except Invite.DoesNotExist:
                form.save()
                return HttpResponseRedirect(reverse(
                    'course_detail', kwargs={'pk': course.id}))

    return render(request, "personal/generic_form.html", {
            'header': 'Invite for ' + str(course), 'form': form}
        )


@login_required()
def course_detail(request, pk):
    ''' Detail view for course. Restricts view to authenticated users who are
    taking the course (as a student or grader) or teaching the course.
    '''
    try:
        user_levels = Takes.objects.filter(course_id=pk, username=request.user)
        if len(user_levels) > 1:
            course = Courses.objects.filter(pk=pk)[0]
        else:
            course = Courses.objects.get(pk=pk)
    except Courses.DoesNotExist:
        raise Http404('Course does not exist.')
    try:
        if course.instructor_username != request.user:
            Takes.objects.get(course_id=pk, username=request.user)
    except Takes.DoesNotExist:
        raise PermissionDenied("You do not have permission \
            to view this course.")

    return render(request, 'personal/course_detail.html', {'course': course})

# INVITES #####################################################################


class InviteDelete(DeleteView):
    ''' Deletes a course, forces confirmation of delete. Throws error for users
    who try to delete a course for which they are not the instructor.
    '''
    model = Invite
    template_name = "personal/confirm_delete.html"
    success_url = reverse_lazy('homepage')

    def get_object(self, *args, **kwargs):
        invite = super(InviteDelete, self).get_object(*args, **kwargs)
        group = Group.objects.get(name="Admin")
        is_admin = True if group in self.request.user.groups.all() else False

        if invite.rec_username != self.request.user and not is_admin:
            raise PermissionDenied("You don't have permission \
                to delete this invitation.")
        return invite

# Generates a random password to give the student before he/she/it
# changes it to something that django will probably reject.
# at least a couple times.
def password_generate():
    password = User.objects.make_random_password()
    return password
# Alex Pendell :: April 9th, 2019


def email(request):
    '''
    View for sending email invites to users. Generates a random password to be
    sent via email, checks to see if supplied email is a potsdam address.
    '''

    if request.method == 'POST':
        newpassword = password_generate()
        recipient = request.POST['user']
        alias = recipient[0:recipient.find('@')]

        # Validate whether email is from potsdam.edu and throw 403 if not
        if recipient[recipient.find('@'):] != '@potsdam.edu':
            raise PermissionDenied("Only potsdam.edu email addresses \
                are allowed.")
        elif User.objects.filter(username=alias).exists():
            # Check if user already exists
            print("There's a snake in my boot.")
        else:
            # Send an email invite if new user
            send_mail(
                'Invite to join the Potsdam Autograder',  # The email title
                'This is an autograder message. Your password is: '
                + newpassword,  # The content.
                settings.EMAIL_HOST_USER,  # The sender
                [recipient],  # The recipient
                fail_silently=False)  # Whether or not we want to see errors

            # This bit will create the account for the user #
            User.objects.create_user(
                username=alias,
                email=recipient,
                password=newpassword)

    return render(request, 'personal/email_form.html')
# Alex :: April 9th, 2019
