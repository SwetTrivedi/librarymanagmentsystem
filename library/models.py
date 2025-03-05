from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Author(models.Model):
    author_name=models.CharField(max_length=70)
    def __str__(self):
        return self.author_name

class Book(models.Model):
    book_name=models.CharField(max_length=200)
    authors=models.ManyToManyField(Author)
    publish_year=models.DateField()
    def written_by(self):
        return "  , ".join([str(p) for p in self.authors.all()])
    def __str__(self):
        return self.book_name

# class Feedback(models.Model):
#     Comment=models.CharField(max_length=200)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.book

    # def __str__(self):
    #     return f"{self.user.username} liked {self.book.book_name}"
   