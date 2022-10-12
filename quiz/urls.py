from django.contrib import admin
from django.urls import path,include
from quiz import views

urlpatterns = [
    path("", views.home),
    path('login', views.login),
    path('signup', views.signup),
    path('confirmlogin', views.confirmlogin),
    path('confirmsignup', views.confirmsignup),
    path('createtable', views.createtable),
    path('selectsub', views.selectsub),
    path('quiz', views.quiz)
]