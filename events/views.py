from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
from django.db.models import Q

from .forms import SignupForm, SigninForm, EventForm, ProfileForm, UserForm, BookEventForm, TicketForm
from .models import Event, Category
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
                # if the user has event then he is an organizer 
                # if not he is a guest and redirect to homepage
                # to see upcommin events
                if request.user.events == None:
                    return redirect('dashboard')
                return redirect('homepage')

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
    categories = Category.objects.all()
    # events = Event.objects.all(start_date__gte = datetime.now() )
    current_events = Event.objects.filter(start_date__lte = datetime.now() , end_date__gte = datetime.now() )
    upcomming_events = Event.objects.filter(start_date__gte = datetime.now() )
    context = {
        'categories':categories,
        # 'events':events,
        'current_events':current_events,
        'upcomming_events': upcomming_events,
    }

    return render(request, 'basics/homepage.html', context)

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
        if form.is_valid():
            event_obj = form.save(commit=False)
            # event_obj.manager = request.user
            event_obj.save()
            return redirect('event-list')
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
        'event': event_obj,
    }
    return render(request, 'event/event_edit.html', context)

def event_book(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    # if event_obj.seats == 0 
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():

            num_of_seats_to_book = int(form.cleaned_data['tickets'])
            # validates the num_of_seats_to_book if less than 0
            if seats_available_validate(event_obj, num_of_seats_to_book):
                # should give a message that the number of seats not available
                return redirect('dashboard')

            ticket = form.save(commit=False)
            # decrease the number of tickets in the event
            event_obj.seats -= num_of_seats_to_book
            event_obj.save()
            # saves the ticket
            ticket.event = event_obj
            ticket.user = request.user
            ticket.save()
            # should redirect to the ticket page to print or save as pdf
            return redirect('event-detail', event_obj.id)

    context = {
        'form': form,
        'event': event_obj,
    }
    return render(request, 'event/event_book.html', context)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#       event validators                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def seats_available_validate(event, seats=0):
    if seats == 0:
        print("-"*50)
        print(event.seats <= 0)
        print("-"*50)
        return event.seats <= 0
    print("X"*50)
    print((seats - event.seats) < 0)
    print("X"*50)
    return (seats - event.seats) > 0
