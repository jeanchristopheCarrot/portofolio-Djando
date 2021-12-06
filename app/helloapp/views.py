from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from requests.models import HTTPError

from helloapp.forms import LogInForm, UpdateForm
from .word import generateWord
from .db import DBConnect
from helloapp import db
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def base(request):
    dbConnection = db.DBConnect()
    currentUser = dbConnection.isCurrentUser()
    if(currentUser == ''):
        loggedin="false"
    else:
        loggedin="true"
    return render(request, 'helloapp/base.html', {'currentUser':currentUser,'loggedin':loggedin})

def game(request):
    print('game')
    try:
        newword = generateWord(); 
        print(newword)
        dbConnection = DBConnect()
        currentUser = dbConnection.isCurrentUser()
        dbConnection.recordWord(newword,currentUser)
        currentScore = dbConnection.isCurrentScore()
        return render(request, 'helloapp/game.html', {'word':newword,'score':currentScore})
    except:
        return HTTPError()
        
    
def login(request):
    return render(request, 'helloapp/login.html', {})

def score(request):
    dbConnection = DBConnect()
    currentUser = dbConnection.isCurrentUser()
    currentScore = dbConnection.isCurrentScore()
    return render(request, 'helloapp/score.html', {'currentUser':currentUser, 'score':currentScore})

def loginForm(request):
    #name = request.form['username']
    #password = request.form['password']
    print('logInForm')
    form = LogInForm(request.POST)
    print(form)
    name = form.cleaned_data['username']
    print(name)
    password = form.cleaned_data['password']
    print(password)
    currentUser = name
    dbConnection = DBConnect()
    if(dbConnection.isUserExists(name)):
        dbConnection.login(name,password)
    else:
        print('register')
        dbConnection.register(name,password)
    return render(request, 'helloapp/base.html', {'currentUser':currentUser,'loggedin':'true'})

def logout(request):
    print('logout')
    dbConnection = db.DBConnect()
    currentUser = dbConnection.isCurrentUser()
    print(currentUser)
    dbConnection.logout(currentUser)
    return render(request, 'helloapp/base.html', {'currentUser':'','loggedin':'false'})

@csrf_exempt
def update(request):
    word = ''
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            letter = form.cleaned_data['letter']
            score = form.cleaned_data['score']
            print('Update');
            print(word);
            print(letter)
            print(score)
    
    dbConnection = DBConnect();
    if(dbConnection.isCurrentUser != None):
        dbConnection.updateScore(score);
        dbConnection.updateWordwithLetter(word,letter);
    #currentUser = session.get('current_user', None)
    #question = get_object_or_404(Question, pk=question_id)
    #try:
    #    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
    #    return render(request, 'polls/detail.html', {
    #        'question': question,
    #        'error_message': "You didn't select a choice.",
    #    })
    #else:
    #    selected_choice.votes += 1
    #    selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    #return render('game.html',word=word)
    return render(request, 'helloapp/game.html', {'word':word})
