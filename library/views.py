from django.shortcuts import render, HttpResponseRedirect
from . forms import Signupform , Loginform
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Book
from django.db.models import Q
# Create your views here.
def home (request):
    return render(request,'home.html')

def signup (request):
    if request.method=="POST":
       form=Signupform(request.POST)
       if form.is_valid():
           messages.success(request,"Your account Created Sucessfully You Are Author!!")
           form.save()
           form=Signupform()
    else:
        form=Signupform()   
    return render (request,'signup.html',{'form':form})



def userlogin(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=Loginform(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Login Sucessfully !!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=Loginform()
        return render (request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
    

def userdashboard(request):
    return render(request,'dashboard.html')

def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/')




def book_search(request):
    query=request.GET.get('q','')
    books=Book.objects.all()
    if query:
        books=Book.objects.filter(Q(book_name__icontains=query) | 
                                  Q(authors__author_name__icontains=query) | 
                                  Q(publish_year__icontains=query))
    return render(request,'book_search.html',{'books':books,'query':query})