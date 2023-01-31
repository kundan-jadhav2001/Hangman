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
    path('setnewpass',views.setnewpass),

    path('selectsub', views.selectsub),

    path('easy_<string>', views.easy),
    path('quiz/<string>', views.clicked),

    path('medium_<string>',views.medium),
    path('quiz_medium/<string>',views.clicked_medium),

    path('savescore',views.savescore),

    path('account',views.account),
    path('logout',views.logout),

]