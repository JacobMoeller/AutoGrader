# Simply installs the the html files that are to be used.

from django.shortcuts import render

def index(request) :
    return render(request, 'personal/home.html')

def homepage(request) :
    return render(request, 'personal/homepage.html')

def contact(request) :
    return render(request, 'personal/basic.html',{'content':['If you would like to contact me, please email me.','moellej200@potsdam.edu']})
