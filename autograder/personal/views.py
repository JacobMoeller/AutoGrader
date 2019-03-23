from personal.models import Invite, Courses, Takes
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from personal.forms import InviteForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


@login_required()
def index(request):
    ''' Dashboard/homepage view. Returns context-based list view of courses
    and invites based on the current user.
    '''
    args = {}
    course_list = None
    invite_list = None
    if request.user.is_authenticated:
        username = request.user.get_username()
        invite_list = Invite.objects.filter(rec_username=username)
        if (request.user.groups.filter(name='Instructor')):
            course_list = Courses.objects.filter(instructor_username=username)

        else:
            take_list = Takes.objects.filter(student_username=username)
            course_list = []
            for take in take_list:
                course_list.append(take.course_id)

    args = {'course_list': course_list, 'invite_list': invite_list}
    return render(request, 'personal/homepage.html', args)


def contact(request):
    return render(
        request, 'personal/basic.html',
        {'content': ['If you would like to contact me, please email me.','moellej200@potsdam.edu']})


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
        obj = super(CoursesUpdate, self).get_object(*args, **kwargs)
        if obj.instructor_username != self.request.user:
            raise PermissionDenied("You don't have permission \
                to edit this course.")
        return obj


class CoursesDelete(DeleteView):
    ''' Deletes a course, forces confirmation of delete. Throws error for users
    who try to delete a course for which they are not the instructor.
    '''
    model = Courses
    success_url = reverse_lazy('homepage')

    def get_object(self, *args, **kwargs):
        obj = super(CoursesDelete, self).get_object(*args, **kwargs)
        if obj.instructor_username != self.request.user:
            raise PermissionDenied("You don't have permission \
                to delete this course.")


@login_required()
def create_invite(request, pk):
    ''' Creates invite for a given course id. Only the current instructor can
    generate an invite for a course.
    '''
    course = get_object_or_404(Courses, pk=pk)
    if course.instructor_username != request.user:
        raise PermissionDenied("You do not have permission \
            to create an invite for this course.")

    if request.method == 'GET':
        rec_list = User.objects.all().exclude(username=request.user)
        form = InviteForm(
            sender_username=request.user,
            course_id=course)

    if request.method == 'POST':
        form = InviteForm(
            sender_username=request.user,
            course_id=course,
            data=request.POST)
        if form.is_valid():
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
    course = Courses.objects.get(pk=pk)
    try:
        if course.instructor_username != request.user:
            Takes.objects.get(course_id=pk, student_username=request.user)
    except Takes.DoesNotExist:
        raise PermissionDenied("You do not have permission \
            to view this course.")

    return render(request, 'personal/course_detail.html', {'course': course})
