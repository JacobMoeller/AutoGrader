from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# Uses signup.html file and UserCreation form to create the sign-in page
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def login(request):
    request.session.set_expiry(300) # session expiers in 5 minutes
    return render(request, 'templates/registration/login.html')
