from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('', views.index, name='homepage'),

    path('course/create/', views.CoursesCreate.as_view(), name='course_create'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:pk>/update/', views.CoursesUpdate.as_view(), name='course_update'),
    path('course/<int:pk>/delete/', views.CoursesDelete.as_view(), name='course_delete'),

    #path('course/<int:pk>/join/', views.accept_invite, name='accept_invite'),
    path('course/invite/<int:pk>', views.create_invite, name='create_invite'),
    #path('course/invite/', views.create_invite, name='create_invite'),
]
