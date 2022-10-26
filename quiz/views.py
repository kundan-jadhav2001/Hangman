from django.shortcuts import render
from django.db import connection
from django.contrib import messages
from random import randint

# Create your views here.
def createtable(request):
    with connection.cursor() as cursor:
        # cursor.execute("create table dwmques(id integer primary key AUTOINCREMENT, question varchar(100), answer varchar(50))")
        cursor.execute("insert into dwmques values(1,'One type of metadata','operational')")
        # cursor.execute("insert into userinfo values('kundan@gmail.com', 'kundan', 'kundan' )")
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

        if username=="" or password == "":
            return render(request, "login.html", {'msg':"Username or Password should not be empty"})
        else:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("select username, pass from userinfo where username = %s", [username])
                    # cursor.execute("select * from userinfo ;")
                    row = cursor.fetchone()
                except:
                    return render(request, 'signup.html',{'msg':'You have no account please create one...'})
                if row!= None or row != "":
                    if username==row[0]:
                        if password==row[1]:
                            return render(request, "selectsub.html", {"username":username, "password":password})
                        else:
                            return render(request, 'login.html',{'msg':"Password is incorrect"})
    return render(request, 'signup.html',{'msg':'You have no account please create one...'})
            

    

def selectsub(request):
    return render(request, 'selectsub.html')

def quiz(request):
    return render(request, 'quiz.html')





def SE(request):
    n=1
    sub = 'SE'
    # n = randint(1, 10)
    with connection.cursor() as cursor:
        try:
            cursor.execute("select question, answer from seques where id = %s", [n])
            row = cursor.fetchone()
        except:
            return render(request, 'quiz.html',{'msg':'Question out of range...','sub':'SE'})
    return render(request, 'quiz.html',{'sub':sub, "question":row[0]})

def IP(request):
    n = randint(1, 10)
    sub = "IP"
    with connection.cursor() as cursor:
        try:
            cursor.execute("select question, answer from ipques where id = %s", [n])
            row = cursor.fetchone()
        except:
            return render(request, 'quiz.html',{'msg':'Question out of range...'})
    return render(request, 'quiz.html',{'sub':sub})

def DWM(request):
    # n = randint(1, 10)
    n=1
    request.session['sub'] = "DWM"
    request.session['lst'] = []
    with connection.cursor() as cursor:
        try:
            cursor.execute("select question, answer from dwmques where id = %s", [n])
            row = cursor.fetchone()
        except:
            return render(request, 'quiz.html',{'msg':'Question out of range...'})
    global answer
    answer = row[1]
    return render(request, 'quiz.html',{'sub':'DWM','question':row[0]})

def CN(request):
    n = randint(1, 10)
    sub = "CN"
    with connection.cursor() as cursor:
        try:
            cursor.execute("select question, answer from cnques where id = %s", [n])
            row = cursor.fetchone()
        except:
            return render(request, 'quiz.html',{'msg':'Question out of range...'})
    return render(request, 'quiz.html',{'sub':sub})

def clicked(request,string):
    x = request.path
    letter = x[len(x)-1:]
    request.session.get('lst').append(letter)
    print(request.session.get('lst'))
    sub = request.session.get('sub')
    if letter in answer:
        print(answer)
    
    return(render(request, 'quiz.html', {'sub':sub,'url':'letteronly',"lst":request.session.get('lst')}))