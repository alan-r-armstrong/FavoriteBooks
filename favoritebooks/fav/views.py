from django.http import request
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method =="GET":
        return redirect('/')
    errors = User.objects.validators(request.POST)
    if errors:
        for x in errors.values():
            messages.error(request, x)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, 'account registered')
        return redirect('/')

def login(request):
    if request.method=="GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid login, try again')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    print("logged in")
    return redirect('/home')

def home(request):
    if 'user_id' in request.session:
        form = BookForm()
        context = {
            "user" : User.objects.get(id=request.session['user_id']),  
            "bookform" : form,
            'book': Book.objects.all(),
        }
        return render(request, "home.html", context)
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def addbook(request):
    errors = Book.objects.validators(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
    else:
        uploaded_by = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title=request.POST['title'], 
            author=request.POST['author'], 
            description=request.POST['description'],
            uploaded_by = uploaded_by
        )
        uploaded_by.liked_books.add(book)
        print('this was addbook')
        return redirect(f"/home/{book.id}")

def book(request, book_id):
    form = BookForm()
    context = {
        'book': Book.objects.get(id=book_id),
        'user': User.objects.get(id=request.session['user_id']),
        'bookform' : form,
    }
    return render(request, "book.html", context)

def editbook(request, book_id):
    # if uploaded_by.id = User.id, allow only the uploader of a book to edit it.
    # if User.objects.id == Book.objects.uploaded_by.user.id:
    errors = Book.objects.validators(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
    book = Book.objects.get(id=book_id)
    book.title = request.POST['title']
    book.author = request.POST['author']
    book.description = request.POST['description']
    book.save()
    print('this was editbook')
    return redirect(f'/home/{book_id}')

def delete(request, book_id):
    if request.method == "GET":
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect("/home")

def favorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user.liked_books.add(book)

    return redirect(f'/home/{book_id}')

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user.liked_books.remove(book)

    return redirect(f'/home/{book_id}')