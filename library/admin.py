from django.contrib import admin
from .models import Author
# Register your models here.
from .models import Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['id','author_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=['id','book_name','publish_year','written_by']