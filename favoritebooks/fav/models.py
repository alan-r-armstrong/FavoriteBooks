from django.db import models
import re
from datetime import datetime
import bcrypt
from django.db.models.fields import EmailField, related

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def validators(self, postData):
        errors = {}
        # email address valid check
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address, please re-enter'
        # email already exist in DB check
        email_exist = User.objects.filter(email=postData['email'])
        if email_exist:
            errors['dupe'] = 'email address already exists, please enter different email'
        # user name validation
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name needs to be at least 2 character"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name needs to be at least 2 character"
        # password validation
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Password does not match, please try again'
        return errors
    def register(self, postData):
        encpassword = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = encpassword,
        )
    def authenticate(self, email, password):
        user = User.objects.filter(email=email)
        if user:
            user = user[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
            else:
                return False
        return False

class User(models.Model):
    first_name = models.TextField(max_length=255)
    last_name = models.TextField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def validators(self, postData):
        errors = {}
        # book name validation
        if len(postData['title']) < 1:
            errors['title'] = "title needs to be at least 1 character"
        if len(postData['description']) < 5:
            errors['description'] = "Description needs to be at least 5 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(null=True, max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
        #the user who uploaded a given book
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
        #a list of users who like a given book
    objects = BookManager()

