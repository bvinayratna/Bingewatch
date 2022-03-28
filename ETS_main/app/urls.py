from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.layout, name='layout'),
    path('home/', views.home, name='homepage'),
    path('login/', views.login, name ='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/',views.logout,name='logout'),
    path('exportcsv/',views.exportcsv),
    path('watch/', views.watch, name='watch'),
    path('play/', views.play, name='play'),
    path('listen/', views.listen, name='listen')
]
