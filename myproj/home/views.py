from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import MyRegistrationForm
from django.contrib.auth.models import Group

def home(request):
    # get groups for test
    return render(request, 'base.html', {'groups': Group.objects.all()})

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        for g in user.groups.all():
            print(g, type(g))
        return redirect('/')
    return render(request, 'login.html', {'error':'invalid username or password'})

@login_required(login_url='/home/login')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form':MyRegistrationForm()})
    form = MyRegistrationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        auth.login(request, user)
        return redirect('/')
    return render(request, 'register.html', {'form':form})