# Simply installs the the html files that are to be used.
from django.contrib.auth.models import User, Group
from personal.models import *
from django.shortcuts import render

# User index page
# Parameter: request for template render
# Returns: render of homepage
def index(request) :
    return render(request, 'personal/home.html')

# User homepage
# Parameter: request for template render
# Returns: render of homepage, which contains course and invite list
def homepage(request) :
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
            invite = Invite.objects.get(id = invite_id)

            # determines if invite is for grader/student
            grader_flag = False
            if (invite.level_of_invite == 'g'):
                grader_flag = True
            # Places user into course specified in invite model
            Takes.objects.create(
                student_username=request.user,
                course_id=Courses.objects.get(id = invite.course_id.id),
                is_grader_in_course = grader_flag)
            # Removes invite instance, so it cannot be accepted multiple times
            Invite.objects.filter(id = invite_id).delete()

        # gets username for current user
        username = request.user.get_username()
        # gets current list of invites for user
        invite_list = Invite.objects.filter(rec_username = username)
        # Gets list of courses; This depends on whether user is instructor or student
        if (request.user.groups.filter(name='Instructor')):
            course_list = Courses.objects.filter(instructor_username = username)

        else:
            take_list = Takes.objects.filter(student_username = username)
            course_list = [];
            for take in take_list:
                course_list.append(take.course_id)

    # gives the render context
    args = {'course_list': course_list, 'invite_list': invite_list}

    return render(request, 'personal/homepage.html', args)

# Contact page
# Parameter: request for template render
# Returns: render of contact page
def contact(request) :
    return render(request, 'personal/basic.html',{'content':['If you would like to contact me, please email me.','moellej200@potsdam.edu']})
