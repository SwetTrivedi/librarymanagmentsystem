from django.contrib import admin
from .models import Author
# Register your models here.
from .models import Book ,Rating,Comment,Like,favourite

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['id','author_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=['id','book_name','publish_year','book_cate','written_by','book_rating']

# @admin.register(Feedback)
# class FeedbackAdmin(admin.ModelAdmin):
#     list_display=['comment']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display=['user','book','score']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['user','book','text','total_likes']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display=['user','book']

@admin.register(favourite)
class FavAdmin(admin.ModelAdmin):
    list_display=['user','book']