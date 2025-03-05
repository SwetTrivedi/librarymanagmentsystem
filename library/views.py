from django.shortcuts import render, HttpResponseRedirect,redirect
from . forms import Signupform , Loginform  ,  Addbook ,Usercomment
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Book ,  Rating, Like
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
                    if  user.is_superuser:
                        return HttpResponseRedirect('/admindashboard/')
                    else:
                        books=Book.objects.all().order_by('id')
                        return render(request,'dashboard.html',{'books':books})

        else:
            form=Loginform()
        return render (request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
    

def admindashboard(request):

    return render(request,'admindashboard.html')


def userdashboard(request):
    user=request.user
    full_name=user.get_full_name()
    return render(request,'dashboard.html',{'fullname':full_name})

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




def book_list(request):
        books=Book.objects.all().order_by('id')
        return render(request,'booklist.html',{'books':books})

def viewbooks(request,pk):
    book=Book.objects.get(pk=pk)
    return render(request,'bookdetails.html',{'book':book})


def addbook(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=Addbook(request.POST)
            if form.is_valid():
                book=form.save(commit=False)
                book.save()
                book.authors.set(form.cleaned_data['authors'])
                form= Addbook()
    
        else:
            form= Addbook()
        return render(request,'addnewbook.html',{'forms':form})


def updatebook(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Book.objects.get(pk=id)
            form=Addbook(request.POST,instance=pi)
            if form.is_valid():
                book=form.save(commit=False)
                book.save()
                book.authors.set(form.cleaned_data['authors'])
                form=Addbook
        else:
            pi=Book.objects.get(pk=id)
            form=Addbook(instance=pi)
        return render(request,'update.html',{'form':form})


def deletebook(request,pk):
    pi=Book.objects.get(pk=pk)
    pi.delete()
    return HttpResponseRedirect('/booklist/')


def feedback_page(request):
    return render(request,'feedback.html')




def addcomment(request,id):
        if request.method=="POST":
            pi=Book.objects.get(pk=id)
            form=Usercomment(request.POST)
            if form.is_valid():
                comment=form.save(commit=False)
                comment.user=request.user
                comment.book=pi
                comment.save()
                form=Usercomment()
        else:
            form=Usercomment()
        return render(request,'comment.html',{'form':form})




def rate_book(request, pk ,score):
    book = Book.objects.get(pk=pk)
    Rating.objects.update_or_create(user=request.user, book=book, defaults={'score': score})
    return render(request, 'bookdetails.html', {'book': book})




def book_like(request, pk):
    book = Book.objects.get(pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, book=book)
    if not created:
        like.delete()
    total_likes = book.like_set.count()
    user_has_liked = book.like_set.filter(user=request.user).exists()
    return render(request, 'bookdetails.html', {'book': book,'total_likes': total_likes,'user_has_liked': user_has_liked})