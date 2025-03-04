from django.contrib import admin
from .models import Author
# Register your models here.
from .models import Book ,Feedback

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['id','author_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=['id','book_name','publish_year','written_by']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display=['comment']