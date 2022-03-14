import django
from django.shortcuts import redirect, render
from .models import user
from django.http import HttpResponse



# Create your views here.
def layout(request):
    return render(request, "app/layout.html")

def home(request):
    return render(request, "app/home.html")

def login(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('password'):
            try:
                User = user.objects.get(username=request.POST.get('username'))
            except:
                User=None
                User = user.objects.filter(username=request.POST.get('username'))
            if User:
                if User.password==request.POST.get('password'):
                    return HttpResponse("Login Successful")
                else: 
                    return redirect('login')
            else: 
                    return redirect('signup')
    else:
        return render(request, "app/login.html")

def signup(request):
	if request.method=='POST':
		if request.POST.get('username') and request.POST.get('password') and request.POST.get('fullname') and request.POST.get('email'):
			User=user()
			User.username=request.POST.get('username')
			User.password=request.POST.get('password')
			User.fullname=request.POST.get('fullname')
			User.email=request.POST.get('email')
			User.save()
			return redirect('login')
	else:
		return render(request, "app/signup.html")