from django.urls import path, include
from .views import home, register, login, logout, dashboard, display_books, display_user_books, add_book, remove_book, book_details, write_review

app_name = 'books'
urlpatterns = [
    path('', home, name='home'),
    path(r'create-account/', register, name='register'),
    path(r'my-login/', login, name='login'),
    path(r'logout/', logout, name='logout'),
    path(r'my-dashboard/', dashboard, name='dashboard'),
    path(r'browse/', display_books, name='display_books'),
    path(r'my-library/', display_user_books, name='display_user_books'),
    path(r'add/<int:book_id>/', add_book, name='add_book'),
    path(r'remove/<int:book_id>/', remove_book, name='remove_book'),
    path(r'details/<int:book_id>/', book_details, name='book_details'),
    path(r'write-review/<int:book_id>/', write_review, name='write_review'),
]