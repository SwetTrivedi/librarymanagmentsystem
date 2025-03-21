from django.shortcuts import render, HttpResponseRedirect,redirect,HttpResponse
from . forms import Signupform , Loginform  ,  Addbook ,Usercomment,RatingForm,Borrowform
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Book ,  Rating, Like , Comment ,favourite
from django.db.models import Q , Avg
from django.core.paginator import Paginator
from django .shortcuts import get_object_or_404
from django.conf import settings
import os
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
        allpost=Book.objects.all().order_by('id')
        paginator=Paginator(allpost,5)
        pageno=request.GET.get('page')
        pageobj=paginator.get_page(pageno)

        return render(request,'booklist.html' ,{'books':pageobj})
     

def viewbooks(request,pk):
    book=Book.objects.get(pk=pk)
    user_rating =Rating.objects.filter(book=book, user=request.user).first()
    user_has_borrowed = book.borrowrecord_set.filter(user=request.user, is_returned=False).exists()
    print(user_has_borrowed)
    borrowed_books_count = BorrowRecord.objects.filter(user=request.user, is_returned=False).values('book').distinct().count()
    user_reached_limit = borrowed_books_count >=5
    if request.method=='POST':
        text=request.POST.get('text')
    
        if text:
            Comment.objects.create(user=request.user,book=book,text=text)
            return redirect('viewsbook',pk=pk)
    return render(request,'bookdetails.html',{'book':book , 'user_has_borrowed':user_has_borrowed ,'user_reached_limit':user_reached_limit, 'user_rating':user_rating})

def addbook(request):
    # if request.user.is_authenticated:
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
            book=Book.objects.get(pk=id)
            comments = book.comment_set.all()
            if request.method == "POST":
                text = request.POST.get("text","").strip()
                if text:
                    Comment.objects.create(book=book, user=request.user,text=text)
                    return redirect('comment', id=book.id)
            return render(request,'comment.html',{'alldata':comments ,'book':book})


def book_like(request, id):
        comment = Comment.objects.get(pk=id)
        if request.user.is_authenticated:
            if request.user in comment.likes.all():
                comment.likes.remove(request.user)  
            else:
                comment.likes.add(request.user)

        return redirect('comment', id=comment.book.id)



def deletecomment(request, id):
    pi = get_object_or_404(Comment, id=id)
    if request.user.is_superuser or request.user == pi.user:
        pi.delete()
        return HttpResponseRedirect('/booklist/')
    else:
        return HttpResponse("You are not allowed to delete this comment.", status=403)

def add_rating(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['book_rating']
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'score': rating_value}
            )
            return redirect('viewsbook', pk=pk)
    else:
        form = RatingForm()
    return render(request, 'rate_book.html', {'form': form, 'book': book })



def fav_book(request, book_id):
    book = Book.objects.get(pk=book_id) 
    fav, created = favourite.objects.get_or_create(user=request.user, book=book)
    if not created:
        fav.delete() 
    return redirect('booklist') 

def favorite_books(request):
    fav_books = Book.objects.filter(favourite_book__user=request.user) 
    return render(request, 'favoirate.html', {'fav_books': fav_books})



from .models import Book, BorrowRecord
from datetime import date
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    already_borrowed = BorrowRecord.objects.filter(user=request.user, book=book, is_returned=False).exists()
    if already_borrowed:
        messages.error(request, f"You have already borrowed '{book.book_name}'.")
    if request.method=="POST":
        form=Borrowform(request.POST)
        if form.is_valid():
            if book.available_copies > 0:
                borrow = BorrowRecord.objects.create(user=request.user, book=book)
                book.available_copies -= 1
                book.save()
                
                messages.success(request, f"You have borrowed '{book.book_name}'. Return by {borrow.due_date}.")
            else:
                messages.warning(request, "Sorry, this book is currently not available.")
    else:
        form=Borrowform()  
    return render(request,'borrow.html',{"form":form})


def return_book(request, borrow_id):
    borrow = get_object_or_404(BorrowRecord, id=borrow_id, user=request.user)

    if not borrow.is_returned:
        borrow.is_returned = True
        borrow.return_date = date.today()
        borrow.book.available_copies += 1
        borrow.book.save()
        borrow.save()

        messages.success(request, f"You have successfully returned '{borrow.book.book_name}'.")
    else:
        messages.warning(request, "This book is already returned.")

    return redirect('home')

def my_borrowed_books(request):
    borrowed_books = BorrowRecord.objects.filter(user=request.user)
    returned_books = borrowed_books.filter(is_returned=True)
    not_returned_books = borrowed_books.filter(is_returned=False)  

    return render(request, 'borrowed.html', {
        'borrowed_books':borrowed_books,
        'not_returned_books': not_returned_books,
        'returned_books': returned_books
        })
