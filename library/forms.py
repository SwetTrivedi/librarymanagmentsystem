from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from .models import Book,Author,Comment, BorrowRecord

class Signupform(UserCreationForm):
    password1=forms.CharField(label="Password" ,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label=" Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels={'first_name':'First Name','last_name':'Last Name','email':'Email'}

        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),
                'first_name':forms.TextInput(attrs={'class':'form-control'}),
                'last_name':forms.TextInput(attrs={'class':'form-control'}),
                'email':forms.EmailInput(attrs={'class':'form-control'})}



class Loginform(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(label=_("Password"),
                             strip=False,widget=forms.PasswordInput
                             (attrs={'autocomplete':'current-password','class':'form-control'})) 
    

# class Addbook(Book):
#     class Meta:
#         model=Book
#         fields=['book_name','publish_year','authors']



class Addbook(forms.ModelForm):
    authors = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter authors name'}),
    help_text = 'Enter multiple authors by separeted by commas'
    )
    publish_year = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    book_cate=forms.CharField(label="Book Category" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Book Category'}))
    class Meta:
        model = Book    
        fields = ['book_name', 'authors', 'publish_year','book_cate']
        widgets = {
            'book_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            }
    def clean_authors(self):
   
        data = self.cleaned_data['authors']
        author_name= [name.strip() for name in data.split(',') if name.strip()]  

        if not author_name:
            raise forms.ValidationError("Please enter at least one author.")

        authors = []
        for name in author_name:
            author, created = Author.objects.get_or_create(author_name=name)  
            authors.append(author)  

        return authors
    

class Usercomment(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']
        labels={'text':'Comment'}
        widgets={'text':forms.Textarea(attrs={'class': 'form-control'})}



class RatingForm(forms.Form):
    book_rating = forms.FloatField(
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={'step':0.1}))

class Borrowform(forms.ModelForm):
    class Meta:
        model=BorrowRecord
        fields=['book','return_date','due_date']
        widgets={
                'book': forms.Select(attrs={'class': 'form-control'}),
                'return_date':forms.TextInput(attrs={'class':'form-control'}),
               'due_date':forms.TextInput(attrs={'class':'form-control'}),
        }
