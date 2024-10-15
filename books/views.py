from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book, User, Review
from .forms import UserRegistrationForm, UserLoginForm
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.db import connection, transaction

def home(request):
    return render(request, 'books/home.html')

def register(request):
    context={}
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.user
            return redirect('books:dashboard')
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
                return redirect('books:dashboard')
        else:
            context['login_form']=form
    else:
        form=UserLoginForm()
        context['login_form']=form
    return render(request, 'books/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('books:home')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('books:login')
    user = request.user
    account_date = user.account_date.date()
    return render(request, 'books/dashboard.html', {'user' : user})

def display_books(request):
    books = Book.objects.all()
    return render(request, 'books/display_books.html', {'books' : books})

def display_user_books(request):
    if not request.user.is_authenticated:
        return redirect('books:login')
    user = request.user
    user = User.objects.get(username=user.username)
    user_books = user.books.all()
    return render(request, 'books/display_user_books.html', {'user_books' : user_books})

def add_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('books:login')
    user = request.user

    cursor = connection.cursor()
   
    cursor.execute("SELECT book_id FROM books_user_books WHERE user_id=%s", [user.id])
    id_books = cursor.fetchall()
    for id_book in id_books:
        if id_book[0] == book_id:
            return redirect('books:display_user_books')

    cursor.execute("SELECT num_hits FROM books_book WHERE id=%s", [book_id])
    num_hits = cursor.fetchone()
    cursor.execute("UPDATE books_user SET num_books=%s WHERE id=%s", [user.num_books+1, user.id])
    cursor.execute("UPDATE books_book SET num_hits=%s WHERE id=%s", [num_hits[0]+1, book_id])
    cursor.execute("INSERT INTO books_user_books(user_id, book_id) VALUES (%s, %s)", [user.id, book_id])

    transaction.commit()

    return redirect('books:display_user_books')
    

def remove_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('books:login')
    user = request.user
    
    cursor = connection.cursor()

    cursor.execute("SELECT num_hits FROM books_book WHERE id=%s", [book_id])
    num_hits = cursor.fetchone()
    cursor.execute("UPDATE books_user SET num_books=%s WHERE id=%s", [user.num_books-1, user.id])
    cursor.execute("UPDATE books_book SET num_hits=%s WHERE id=%s", [num_hits[0]-1, book_id])
    cursor.execute("DELETE FROM books_user_books WHERE user_id=%s AND book_id=%s", [user.id, book_id])
    
    transaction.commit()

    return redirect('books:display_user_books')

def book_details(request, book_id):
    book = Book.objects.get(pk=book_id)
    reviews = Review.objects.filter(book=book_id).order_by('-pub_date')
    return render(request, 'books/book_details.html', {'book' : book, 'reviews' : reviews})

def write_review(request, book_id):
    if not request.user.is_authenticated:
        return redirect('books:login')
    if request.method == 'POST':
        user = request.user

        cursor = connection.cursor()

        cursor.execute("SELECT ratings_count FROM books_book WHERE id=%s", [book_id])
        ratings_count = cursor.fetchone()
        cursor.execute("UPDATE books_user SET num_reviews=%s WHERE id=%s", [user.num_reviews+1, user.id])
        cursor.execute("UPDATE books_book SET ratings_count=%s WHERE id=%s", [ratings_count[0]+1, book_id])
        
        rating = request.POST.get('rating')
        
        cursor.execute("SELECT ratings_avg FROM books_book WHERE id=%s", [book_id])
        ratings_avg = cursor.fetchone()
        ratings_avg = int(((ratings_avg[0]*ratings_count[0] + int(rating)) / (ratings_count[0])) * 100)
        ratings_avg = ratings_avg/100.0
        cursor.execute("UPDATE books_book SET ratings_avg=%s WHERE id=%s", [ratings_avg, book_id])

        if request.POST.get('review'):
            review_text = request.POST.get('review')
            cursor.execute("SELECT reviews_count FROM books_book WHERE id=%s", [book_id])
            reviews_count = cursor.fetchone()
            cursor.execute("UPDATE books_book SET reviews_count=%s WHERE id=%s", [reviews_count[0]+1, book_id])
        else:
            review_text = ''
        
        transaction.commit()

        review = Review(book=Book.objects.get(pk=book_id), user=user, rating=rating, review_text=review_text)
        review.save()
        
        return redirect("books:book_details", book_id)
    return render(request, 'books/write_review.html') 