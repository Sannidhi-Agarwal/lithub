from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, User, Review

# Register your models here.

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Review)