from django.shortcuts import render
from django.db import connection
from django.contrib import messages

# Create your views here.
def createtable(request):
    with connection.cursor() as cursor:
        cursor.execute("insert into userinfo values('kundan@gmail.com', 'kundan', 'kundan' )")
        # cursor.execute("drop table userinfo")
        # cursor.execute("create table userinfo(email Varchar(30), pass varchar(20), username varchar(20) primary key)")


    

def home(request):
    return render(request, 'home.html',{"msg":""})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def confirmsignup(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpass = request.POST['confpass']

        with connection.cursor() as cursor:
            cursor.execute("select username from userinfo where username = %s", [username])
            # cursor.execute("select * from userinfo ;")
            row = cursor.fetchone()
            if row == None:
                cursor.execute("insert into userinfo values(%s,%s,%s);",[email,password,username])
                msg = 'Profile details added to database.'
                return render(request, "home.html", {"msg":msg})
                
            else:
                msg = 'Username already exist try something new'

    return render(request, "signup.html", {"msg":msg})

        
    

def confirmlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password'] 

        with connection.cursor() as cursor:
            cursor.execute("select username, pass from userinfo where username = %s", [username])
            # cursor.execute("select * from userinfo ;")
            row = cursor.fetchone()
            if username==row[0]:
                if password==row[1]:
                    return render(request, "quiz.html", {"username":username, "password":password})
                else:
                    return render(request, 'signup.html',{'msg':"Wrong Password is incorrect"})

            

    return render(request, 'signup.html',{'msg':'You have no account please create one...'})

def selectsub(request):
    return render(request, 'selectsub.html')

def quiz(request):
    return render(request, 'quiz.html')