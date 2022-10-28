from django.shortcuts import render
from django.db import connection
from django.contrib import messages
from random import randint

# Create your views here.
def createtable(request):
    with connection.cursor() as cursor:
        # cursor.execute("create table dwmques(id integer primary key AUTOINCREMENT, question varchar(100), answer varchar(50))")
        cursor.execute("insert into dwmques values(2,'Kind of system required for data warehouse','sourcesystem')")
        cursor.execute("insert into dwmques values(3,'It contains non-volatile data','OLAP')")
        cursor.execute("insert into dwmques values(4,'data warehouse is application','independent')")

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
    n = randint(1, 4)
    request.session['sub'] = "DWM"
    
    with connection.cursor() as cursor:
        try:
            cursor.execute("select question, answer from dwmques where id = %s", [n])
            row = cursor.fetchone()
        except:
            return render(request, 'quiz.html',{'msg':'Question out of range...'})
    
    global question, answer, ansstr, lst, tries
    tries = 0
    lst = []
    answer = row[1].lower()
    ansstr = "_" * len(answer)
    question = row[0]
    return render(request, 'quiz.html',{'sub':'DWM','question':question,'len_ans':len(answer)})

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
    global lst, ansstr, tries
    if tries==3:
        return(render(request, "loss.html"))
    
    len_ans = len(answer)
    x = request.path
    letter = x[len(x)-1:]
    lst.append(letter)
    sub = request.session.get('sub')
    occurences = [i for i in range(len_ans) if answer.startswith(letter, i)]

    if ansstr==answer:
        return(render(request, 'won.html',{'sub':sub}))

    for i in occurences:
        ansstr = ansstr[:i] + answer[i] + ansstr[i+1:]

    if len(occurences)==0:
        tries += 1

    
    return(render(request, 'quiz.html', {'sub':sub,'question':question, 'url':'letteronly',"lst":lst,'len_ans':len_ans,'ansstr':ansstr}))