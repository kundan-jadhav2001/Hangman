from django.shortcuts import render
from django.db import connection
from django.contrib import messages
from random import randint
import smtplib

# Create your views here.
def createtable(request):
    with connection.cursor() as cursor:
        pass
        # cursor.execute("create table cnques(id integer primary key AUTOINCREMENT, question varchar(100), answer varchar(50))")

        # cursor.execute("insert into cnques values(1,'What is used for remote logging','telnet')")
        # cursor.execute("insert into cnques values(2,'What is used for remote logging in secured manner','ssh')")
        
        
        # cursor.execute("drop table userinfo;")
        # cursor.execute("create table userinfo(name Varchar(100), username varchar(20) primary key, email Varchar(50), pass Varchar(20),avatar Varchar(10));")


def home(request):
    try:
        if request.session['userlogedin']:
            return render(request, 'home.html',{"msg":"",'userlogedin':request.session['userlogedin']})
    except:
        return render(request, 'home.html',{"msg":""})

def account(request):
    return render(request, 'userdetails.html')

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
                cursor.execute("select username, pass from userinfo where username = %s", [username])
                row = cursor.fetchone()
                if row!= None or row != "":
                    if username == row[0]:
                        if password == row[1]:
                            request.session['userlogedin'] = row[0]
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
    return render(request, 'selectsub.html')

#random question generator for easy level
def subject(request, string):
    sub = string
    print(sub)
    n = randint(1, 4)
    request.session['sub'] = sub

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
    global lst, ansstr, tries
    
    len_ans = len(answer)
    url = request.path
    letter = url[len(url)-1:]
    lst.append(letter)
    sub = request.session.get('sub')
    occurences = [i for i in range(len_ans) if answer.startswith(letter, i)]

    for i in occurences:
        ansstr = ansstr[:i] + answer[i] + ansstr[i+1:]

    if ansstr==answer:
        return(render(request, 'won.html',{'sub':sub}))

    if len(occurences)==0:
        tries -= 1
        
    if tries<1:
        return(render(request, "loss.html"))
    
    return(render(request, 'quiz.html', {'sub':sub,'question':question, 'url':'letteronly',"lst":lst,'len_ans':len_ans,'ansstr':ansstr,'tries':tries}))


def forgotpass(request):
    if request.method == 'POST':

        gmail_user = 'en20133485@git-india.edu.in'
        gmail_password = 'kundan@2001'

        sent_from = gmail_user
        to = request.POST['email']
        with connection.cursor() as cursor:
            try:
                cursor.execute("select email from userinfo where email = %s", [to])
                row = cursor.fetchone()
            except:
                return render(request, 'forgotpass.html',{'msg':"Error occured while connecting to database"})


        subject = 'OTP'
        otp = randint(100000, 999999)
        body = f'The OTP for password reset is {otp}'

        email_text = """
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (sent_from, to, subject, body)
        if row != None:
            try:
                server = smtplib.SMTP('smtp.gmail.com', 465)
                server.starttls()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, email_text)
                server.quit()

                print('Email sent!')
                return(render(request, "newpass.html"))
            except Exception as e:
                print(e)
        else:
            return render(request, 'forgotpass.html',{'msg':"Email not found in database. You don't have accound"})
    return(render(request, "forgotpass.html" ))
    

def newpass(request):
    pass


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
