from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from .forms import SignupForm, SigninForm, EventForm, ProfileForm, UserForm

from .models import Event

#####################################################################
#       auth views                                                  #
#####################################################################

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect("homepage")
    context = {
        "form":form,
    }
    return render(request, 'auth/signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('dashboard')
    context = {
        "form":form
    }
    return render(request, 'auth/signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")


#####################################################################
#       basic views                                                 #
#####################################################################

def homepage(request):
    return render(request, 'basics/homepage.html')

def dashboard(request):
    events = Event.objects.filter(organizer=request.user)
    context = {
        'events': events
    }
    return render(request, 'basics/dashboard.html', context)

def not_found(request):
    return render(request, 'basics/404.html')

def profile(request):
    context = {
        "user": request.user,
    }
    return render(request,'basics/profile.html', context)

def profile_edit(request):
    profile_obj = request.user.profile
    form = ProfileForm(instance=profile_obj)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {
        "form": form,
    }
    return render(request,'basics/profile_edit.html', context)

def user_edit(request):
    user_obj = request.user
    form = UserForm(instance=user_obj)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            # login(request, user)
            return redirect('signin')
            # return redirect('profile')
    context = {
        "form": form,
    }
    return render(request,'basics/user_edit.html', context)


#####################################################################
#       event views                                                 #
#####################################################################

def event_list(request):
    events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, 'event/event_list.html', context)

def event_create(request):    
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid:
            event_obj = form.save(commit=False)
            # event_obj.manager = request.user
            event_obj.save()
            return redirect('event/event_list.html', event_obj.id)
    context = {
        "form": form,
    }
    return render(request, 'event/event_create.html', context)

def event_detail(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    context = {
        'event': event_obj
    }
    return render(request, 'event/event_detail.html', context)

def event_edit(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    form = EventForm(instance=event_obj)
    context = {
        'form': form,
        # 'event': event_obj,
    }
    return render(request, 'event/event_edit.html', context)
