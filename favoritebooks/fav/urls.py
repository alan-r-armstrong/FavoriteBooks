from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('addbook', views.addbook),
    path('home/<int:book_id>', views.book),
    path('home/<int:book_id>/editbook', views.editbook),
    path('home/<int:book_id>/delete', views.delete),
    path('home/<int:book_id>/favorite', views.favorite),
    path('home/<int:book_id>/unfavorite', views.unfavorite),
    path('logout', views.logout),
]