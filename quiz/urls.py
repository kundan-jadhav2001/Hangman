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
    path('forgotpass',views.forgotpass),
    path('newpass',views.newpass),
    path('selectsub', views.selectsub),
    path('quiz', views.quiz),
    path('SE',views.SE),
    path('IP',views.IP),
    path('DWM',views.DWM),
    path('CN',views.CN),
    path('quiz/SE/""',views.clicked),
    path('quiz/CN/""',views.clicked),
    path('quiz/DWM/<string>',views.clicked),
    path('quiz/CN/<string>',views.clicked)

]