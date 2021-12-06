from django.urls import path
from helloapp import views

urlpatterns = [
    path('', views.base, name='base'),
    path('login/', views.login, name='login'),
    path('score/', views.score, name='score'),
    path('game/', views.game, name='game'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('loginForm/', views.loginForm, name='loginForm'),
]