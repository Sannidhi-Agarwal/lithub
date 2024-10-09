from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Navbar, Book, User, Review
from .forms import UserRegistrationForm, UserLoginForm
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def register(request):
    context={}
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.user
            return redirect(dashboard)
        context['register_form']=form
    else:
        form=UserRegistrationForm()
        context['register_form']=form
    return render(request, 'books/register.html', context)

def login(request):
    context={}
    if request.method == 'POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(dashboard)
        else:
            context['login_form']=form
    else:
        form=UserLoginForm()
        context['login_form']=form
    return render(request, 'books/login.html', context)

def logout(request):
    auth_logout(request)
    return render(request, 'books/login.html', context)

def dashboard(request):
    user = request.user
    return render(request, 'books/dashboard.html', {'user' : user})

def display_books(request):
    books = Book.objects.all()
    return render(request, 'books/display_books.html', {'books' : books})

def display_user_books(request):
    user = request.user
    user = User.objects.get(username=user.username)
    user_books = user.books.all()
    return render(request, 'books/display_user_books.html', {'user_books' : user_books})

def add_book(request, book_id):
    user = request.user
    user.add(books = book_id)
    user = User.objects.filter(id=user.id)
    user.num_books += 1
    user.save()

    book = Book.objects.get(pk=book_id)
    book.num_hits +=1
    book.save()

def remove_book(request, book_id):
    user = request.user
    user = User.objects.filter(id=user.id)
    user.filter(books = book_id).delete()
    user.num_books -= 1
    user.save()
    
    book = Book.objects.get(pk=book_id)
    book.num_hits -=1
    book.save()
    return redirect('display_user_books')

def book_details(request, book_object):
    book = book_object
    reviews = Review.objects.filter(book=book).order_by('-pub_date')
    return render(request, 'books/book_details.html', {'book' : book, 'reviews' : reviews})

def write_review(request, book_id):
    return render(request, 'books/write_review.html', book) 

def process_write_review(request, book_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        user_id = request.user
        user = User.objects.filter(id=user_id)
        book = Book.objects.get(pk=book_id)
        user.num_reviews += 1
        book.ratings_count += 1
        if request.POST.get('review'):
            review_text = request.POST.get('review')
            book.reviews_count += 1
        else:
            review_text = ''
        review = Review(book=book_id, user=user_id, rating=rating, review_text=review_text)
        review.save()
        user.save()
        book.save()
        return HttpResponse("Review Submitted!")
    else:
        return HttpResponse("Invalid Request")