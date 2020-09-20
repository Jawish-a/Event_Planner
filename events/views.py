from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout


#####################################################################
#       auth views                                                  #
#####################################################################

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect("homepage")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('homepage')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")


#####################################################################
#       basic views                                                 #
#####################################################################

def homepage(request):
    return render(request, 'basics/homepage.html')

def dashboard(request):
    return render(request, 'basics/dashboard.html')

def not_found(request):
    return render(request, 'basics/404.html')

def profile(request):
    context = {
        "user": request.user,
    }
    return render(request,'basics/profile.html', context)


#####################################################################
#       event views                                                 #
#####################################################################
