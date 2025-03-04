from django.db import models

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
    
class Feedback(models.Model):
    comment=models.CharField(max_length=200)