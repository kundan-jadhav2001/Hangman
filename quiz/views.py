from django.shortcuts import render
from django.db import connection
from django.contrib import messages
from random import randint
import smtplib
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def createtable(request):
    with connection.cursor() as cursor:
        # cursor.execute("create table userinfo(name Varchar(100), username varchar(20) , email Varchar(50), pass Varchar(20),avatar Varchar(10), primary key (username, email));")  
        # cursor.execute("create table cnques(id integer primary key AUTOINCREMENT, question varchar(100), answer varchar(50))")

        # cursor.execute("insert into cnques values(1,'What is used for remote logging','telnet')")
        # cursor.execute("insert into cnques values(2,'What is used for remote logging in secured manner','ssh')")
        
        
        cursor.execute("create table score(username varchar(20) primary key, score integer)")
        # cursor.execute("create table userinfo(name Varchar(100), username varchar(20) primary key, email Varchar(50), pass Varchar(20),avatar Varchar(10));")


def home(request):
    try:
        if request.session['userlogedin']:
            return render(request, 'home.html',{"msg":"",'userlogedin':request.session['userlogedin']})
    except:
        return render(request, 'home.html',{"msg":""})

def account(request):
    username = request.session['userlogedin'][0]
    with connection.cursor() as cursor:
        cursor.execute("select * from userinfo where username = %s;",[username])
        row = cursor.fetchone()
    return render(request, 'userdetails.html', {"username":username, "name":row[0], "email":row[2], "img":row[4]})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html', {"avatar":[1,2,3,4,5,6]})

def confirmsignup(request):
    msg = ""
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        avatar = request.POST['avatar']

        with connection.cursor() as cursor:
            row = cursor.fetchone()
            if row == None:
                cursor.execute("insert into userinfo values(%s,%s,%s,%s,%s);",[name, username, email, password, avatar])
                msg = 'Profile details added to database. Login now'
                return render(request, "login.html", {"msg":msg})
                
            else:
                msg = 'Username already exist try something new'

    return render(request, "signup.html", {"msg":msg})

def confirmlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password'] 

        with connection.cursor() as cursor:
            try:
                cursor.execute("select username, pass, avatar from userinfo where username = %s", [username])
                row = cursor.fetchone()
                if row!= None or row != "":
                    if username == row[0]:
                        if password == row[1]:
                            request.session['userlogedin'] = [row[0], row[2]]
                            return render(request, "selectsub.html")
                        else:
                            return render(request, 'login.html',{'msg':"Password is incorrect"})
            except:
                return render(request, 'signup.html',{'msg':'You have no account please create one...'})
                
    return render(request, 'signup.html',{'msg':'You have no account please create one...'})
            
def logout(request):
    if request.session['userlogedin']:
        del request.session['userlogedin']
    return render(request, 'home.html')
    

def selectsub(request):
    global score
    score = 0
    return render(request, 'selectsub.html')

#random question generator for easy level
def easy(request, string):
    sub = string
    n = randint(1, 4)
    request.session['sub'] = 'easy_' + sub

    global question, answer, ansstr, lst, tries
    tries = 3
    with connection.cursor() as cursor:
        try:
            query = f"select question, answer from {sub}ques where id = {n}"
            cursor.execute(query)
            row = cursor.fetchone()
        except Exception as e:
            print(e)
            return render(request, 'quiz.html',{'msg':'Question out of range...','tries':tries, 'sub':sub})
    lst = []
    ans = list(row[1].lower())
    answer = ""
    
    for i in ans:
        answer = answer + i + " "
    ansstr = "_ " * (len(answer)//2)
    question = row[0]
    return render(request, 'quiz.html',{'sub':sub,'question':question,'len_ans':len(answer),'ansstr':ansstr,'tries':tries})

#which button clicked
def clicked(request,string):
    global lst, ansstr, tries, score
    
    len_ans = len(answer)
    url = request.path
    letter = url[len(url)-1:]
    lst.append(letter)
    sub = request.session.get('sub')
    occurences = [i for i in range(len_ans) if answer.startswith(letter, i)]

    for i in occurences:
        ansstr = ansstr[:i] + answer[i] + ansstr[i+1:]

    if ansstr==answer:
        score += 1
        return render(request, 'won.html',{'sub':sub,"score":score})

    if len(occurences)==0:
        tries -= 1
        
    if tries<1:
        return render(request, "loss.html")
    
    return render(request, 'quiz.html', {'sub':sub,'question':question, 'url':'letteronly',"lst":lst,'len_ans':len_ans,'ansstr':ansstr,'tries':tries})


def forgotpass(request):
    if request.method == 'POST':
        global otp, email
        try:

            entered_otp = request.POST['otp']
            print('trying', entered_otp)
            print(otp)
            if int(entered_otp) == int(otp):
                return render(request, 'newpass.html')
            else:
                return render(request, 'forgotpass.html', {'msg':"OTP didn't matched", 'otp':''})
        except:
            otp = randint(100000, 999999)
            body = f'The OTP for password reset is {otp}'
            
            with connection.cursor() as cursor:
                try:
                    email = request.POST["email"]
                    cursor.execute("select name from userinfo where email = %s", [email])
                    row = cursor.fetchone()
                except Exception as e:
                    return render(request, 'forgotpass.html',{'msg':"Error while connecting to database", 'otp':''})

            if row != None:
                try:
                    send_mail(
                    'OTP',
                    body,
                    'kundanjadhav2001@gmail.com',
                    [f'{request.POST["email"]}'],
                    fail_silently=False,
                    )
                    return(render(request, "forgotpass.html",{'otp':otp}))
                except Exception as e:
                    print(e)
            else:
                return render(request, 'forgotpass.html',{'msg':"Email not found in database. You don't have accound", 'otp':''})
    return(render(request, "forgotpass.html", {'otp':''} ))
    

def setnewpass(request):
    print(email)
    if request.method == "POST":
        newpass = request.post['newpass']
        with connection.cursor() as cursor:
            cursor.execute(f"update userinfo set pass = {newpass} where email = {email};")
            return render(request, 'login.html')
    return render(request, 'forgotpass.html')

#level medium
def medium(request, string):
    sub = string[7:]
    n = randint(1, 4)
    request.session['sub'] = sub

    global question, answer, ansstr, tries
    tries = 3
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"select question, answer from {sub}ques where id = {n}")
            row = cursor.fetchone()
        except Exception as e:
            print(e)
            return render(request, 'quiz_medium.html',{'msg':'Question out of range...','tries':tries, 'sub':sub})
    ans = list(row[1].lower())
    answer = ""
    
    for i in ans:
        answer = answer + i + " "
    ansstr = "_ " * (len(answer)//2)
    question = row[0]
    return render(request, 'quiz_medium.html',{'sub':sub,'question':question,'len_ans':len(answer),'ansstr':ansstr,'tries':tries})

def clicked_medium(request,string):
    global ansstr, tries, answer
    # sub = request.session.get('sub')
    sub = "DWM"

    url = request.path
    letter = url[len(url)-1:]
    
    index = answer.find(letter)
    if index>=0:
        ansstr = ansstr[:index] + answer[index] + ansstr[index+1:]
        answer = answer[:index] + '*' + answer[index+1:]
    else:
        tries -= 1

    if '_' not in ansstr:
        return(render(request, 'won.html',{'sub':sub}))
        
    if tries<1:
        return(render(request, "loss.html"))
    
    return(render(request, 'quiz_medium.html', {'sub':sub,'question':question, 'url':'letteronly', 'ansstr':ansstr,'tries':tries}))

def savescore(request):
    with connection.cursor() as cursor:
        string = f"insert into score values('{request.session['userlogedin'][0]}', {score})"
        cursor.execute(string)
    return render(request, 'selectsub.html')