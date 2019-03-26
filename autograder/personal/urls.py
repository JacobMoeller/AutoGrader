from django.urls import path
from . import views

urlpatterns = [
    # General links
    path('', views.index, name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('index/', views.index, name='homepage'),

    # Course-based links
    path(
        'course/create/',
        views.CoursesCreate.as_view(),
        name='course_create'),
    path(
        'course/<int:pk>/',
        views.course_detail,
        name='course_detail'
        ),
    path(
        'course/<int:pk>/update/',
        views.CoursesUpdate.as_view(),
        name='course_update'
        ),
    path(
        'course/<int:pk>/delete/',
        views.CoursesDelete.as_view(),
        name='course_delete'
        ),

    # Invite-based links
    path(
        'course/invite/<int:pk>',
        views.create_invite,
        name='invite_create'
        ),
    path(
        'invite/<int:pk>/delete/',
        views.InviteDelete.as_view(),
        name='invite_delete'
        ),
    path(
        'email/',
        views.email,
        name='email'
        ),
]
