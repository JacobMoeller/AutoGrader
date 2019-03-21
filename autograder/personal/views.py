# Simply installs the the html files that are to be used.
from django.contrib.auth.models import User, Group
from personal.models import *
from django.shortcuts import render


def index(request) :
    return render(request, 'personal/home.html')

def homepage(request) :
    args = {}
    course_list = None
    invite_list = None
    if request.user.is_authenticated:
        username = request.user.get_username()
        invite_list = Invite.objects.filter(rec_username = username)
        if (request.user.groups.filter(name='Instructor')):
            course_list = Courses.objects.filter(instructor_username = username)

        else:
            take_list = Takes.objects.filter(student_username = username)
            course_list = [];
            for take in take_list:
                course_list.append(take.course_id)

    args = {'course_list': course_list, 'invite_list': invite_list}


    return render(request, 'personal/homepage.html', args)

def contact(request) :
    return render(request, 'personal/basic.html',{'content':['If you would like to contact me, please email me.','moellej200@potsdam.edu']})
