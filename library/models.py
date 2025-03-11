from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import timedelta, date
# Create your models here.
class Author(models.Model):
    author_name=models.CharField(max_length=70)
    def __str__(self):
        return self.author_name

class Book(models.Model):
    book_name=models.CharField(max_length=200)
    authors=models.ManyToManyField(Author)
    publish_year=models.DateField(null=True, blank=True)
    book_cate=models.CharField(max_length=200,null=True, blank=True)
    book_rating=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=0.0)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def written_by(self):
        return "  , ".join([str(p) for p in self.authors.all()])
    def __str__(self):
        return self.book_name




class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(User,related_name='comment_likes', blank=True)
    def total_likes(self):
        return self.likes.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
   

class favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='favourite_book')



class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(default=date.today() + timedelta(days=14))  # 2 weeks
    is_returned = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name}"