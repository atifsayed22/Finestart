from django.http import HttpResponse
from django.shortcuts import render, redirect

def home(req):
    # return HttpResponse("Hello this home page , first response using  in django")
    return render(req,'home.html')

def login(req):
    # return HttpResponse("Hello this about page , first response using  in django")
    return redirect('login')

def signup(req):
    return redirect('signup')
def base(req):
    return render(req,'forms.html')
def demo(req):
    return render(req,'demo.html')