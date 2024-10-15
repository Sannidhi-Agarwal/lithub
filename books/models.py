from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    isbn = models.CharField(max_length=10, default='0')
    isbn13 = models.CharField(max_length=13, default='0')
    language_code = models.CharField(max_length=5)
    num_pages = models.IntegerField()
    num_hits = models.IntegerField(default=0)
    publication_date = models.DateField()
    ratings_count = models.IntegerField(default=0)
    ratings_avg = models.FloatField(default=0)
    reviews_count = models.IntegerField(default=0)
    cover = models.CharField(max_length=20, null=True)

class UserManager(BaseUserManager):
    def create_user(self, username, password, **other_fields):
        if not username:
            raise ValueError("Username required")
        if not password:
            raise ValueError("Password required")
        user=self.model(
            username=self.username,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    account_date = models.DateTimeField(default=timezone.now)
    num_books = models.IntegerField(default=0)
    num_reviews = models.IntegerField(default=0)
    num_friends = models.IntegerField(default=0)
    books = models.ManyToManyField(Book, related_name="users", blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['password']
    objects=UserManager()
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default="DeletedUser", on_delete=models.SET_DEFAULT)
    pub_date = models.DateTimeField("Date of Review", default=timezone.now)
    rating = models.IntegerField(default = 5)
    review_text = models.CharField(max_length=1000)