from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.layout, name='layout'),
    path('home/', views.home, name='homepage'),
    path('login/', views.login, name ='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/',views.logout,name='logout'),
]