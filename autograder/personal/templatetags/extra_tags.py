from django import template
from django.contrib.auth.models import Group
from personal.models import Invite, Assignment, Takes

register = template.Library()


@register.filter
def full_name(user):
    if user.first_name and user.last_name:
        return f'{user.first_name} {user.last_name}'
    return None


@register.filter
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    if group in user.groups.all():
        return True
    return False


@register.filter
def is_instructor(user, course):
    return True if course.instructor_username == user else False


@register.filter
def has_invites(user):
    pending_invites = Invite.objects.filter(rec_username=user).count()
    return pending_invites


@register.filter
def get_assignments(course):
    assignments_list = Assignment.objects.filter(course_id=course)
    return assignments_list


@register.filter
def student_count(course):
    return Takes.objects.filter(course_id=course).count()


@register.filter
def assignment_count(course):
    return Assignment.objects.filter(course_id=course).count()


@register.filter
def student_count(course):
    return Takes.objects.filter(course_id=course).count()


@register.filter
def top_three_recent_assignments(course):
    assignments = Assignment.objects.filter(
        course_id=course).order_by('-due_on')
    return assignments[:3]
