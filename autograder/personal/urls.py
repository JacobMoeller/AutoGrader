#Creates URL for contact

from django.urls import path, include
from . import views

urlpatterns = [
    # path to contact page view
    path('contact/', views.contact, name='contact'),
    # path to index page view
    path('', views.index, name='index'),
    # path to home page view
    path('home/', views.homepage, name='homepage'),
]
