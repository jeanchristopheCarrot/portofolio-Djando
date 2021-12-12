from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from requests.models import HTTPError
from helloapp import db_post

from helloapp.forms import LogInForm, UpdateForm
from .word import generateWord
#from .db import DBConnect
from django.views.decorators.csrf import csrf_exempt
from .models import Users

# Create your views here.

def base(request):
    try:
        if(Users.objects.filter(isCurrentUser=True).exists()):            
            currentUser = Users.objects.get(isCurrentUser=True) 
            return render(request, 'helloapp/base.html', {'currentUser':currentUser,'loggedin':"true"})
        else:
            return render(request, 'helloapp/base.html', {'currentUser':'No User','loggedin':"false"})        
    except:
        return render(request, 'helloapp/base.html', {'currentUser':'NoDatabase','loggedin':'false'})

def game(request):
    try:
        newword = generateWord(); 
        print(newword)        
        currentUser = Users(isCurrentUser=True).name 
        print(currentUser)
        #dbConnection.recordWord(newword,currentUser)
        currentScore = Users(isCurrentUser = True).score
        print(currentScore)
        return render(request, 'helloapp/game.html', {'word':newword,'score':currentScore})
    except:
        return HTTPError()
        
    
def login(request):
    return render(request, 'helloapp/login.html', {})

def score(request):
    currentUser =  Users.objects.get(isCurrentUser = True) 
    currentScore = currentUser.score
    return render(request, 'helloapp/score.html', {'currentUser':currentUser.name, 'score':currentScore})

def loginForm(request):
    print('check form')
    form = LogInForm(request.POST)
    print(form)
    name = form.cleaned_data['username']
    print(name)
    password = form.cleaned_data['password']
    print(password)
    print('check exist')

    if(Users.objects.filter(name=name)):
        print('exist')      
        Users.objects.filter(name=name).update(isCurrentUser = True)
    else:
        print('not exist')
        newUser = Users(name=name, password=password,isCurrentUser = True,score=0)
        newUser.save()
  
    return render(request, 'helloapp/base.html', {'currentUser':name,'loggedin':'true'})

def logout(request):
    print('logout')
    currentUser =  Users.objects.get(isCurrentUser = True) 
    currentUser.isCurrentUser = 0
    currentUser.save()
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
    
    currentUser =  Users.objects.get(isCurrentUser = True) 
    currentUser.score = score
    currentUser.save()


    #dbConnection = db_post.DBConnect();
    #if(dbConnection.isCurrentUser != None):
    #    dbConnection.updateScore(score);
    #    dbConnection.updateWordwithLetter(word,letter);
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
