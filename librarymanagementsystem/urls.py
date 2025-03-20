"""
URL configuration for librarymanagementsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from library import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.userlogin, name='login'),
    path('logout/',views.userlogout, name="userlogout"),
    path('dashboard/',views.userdashboard,name="dashboard"),
    path('admindashboard/',views.admindashboard,name="adminpanel"),
    path('search/',views.book_search,name="searchbook"),
    path('booklist/',views.book_list,name="booklist"),
    path('bookdetail/<int:pk>/',views.viewbooks,name='viewsbook'),
    path('addingnewbook',views.addbook,name='addbook'),
    path('editbook/<int:id>/',views.updatebook,name='editbook'),
    path('bookdelete/<int:pk>/',views.deletebook,name='deletebook'),
    path('feedback',views.feedback_page,name='feedback'),
    path('comments/<int:id>/',views.addcomment,name='comment'),
    path('rate/<int:pk>/',views.add_rating, name='add-rating'),
    path('like/<int:id>/',views.book_like, name='like-book'),
    path('favourite/<int:book_id>/', views.fav_book, name='favbook'),
    path('my-favorites/', views.favorite_books, name='favorite-books'),
    path('deletecomment/<int:id>/', views.deletecomment, name='delcomment'),
    path('borrow/<int:book_id>/',views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    # path('ret/', views.borrowed_book, name='borro_book'),
    # path('rating/', views.averagerating, name='average'),
    path('borrowed-books/', views.borrowed_books, name='borrowed_books'),
]
