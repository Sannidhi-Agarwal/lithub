from django.urls import path, include
from .views import register, login, logout, dashboard, display_books, display_user_books, add_book, remove_book, book_details, write_review

app_name = 'books'
urlpatterns = [
    path('create-account/', register, name='register'),
    path('my-login/', login, name='login'),
    path('', logout, name='logout'),
    path('my-dashboard', dashboard, name='dashboard'),
    path('browse/', display_books, name='display_books'),
    path('my-library/', display_user_books, name='display_user_books'),
    path('', add_book, name='add_book'),
    path('', remove_book, name='remove_book'),
    path('details/', book_details, name='book_details'),
    path('write-review/', write_review, name='write_review'),
]