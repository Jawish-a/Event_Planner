from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
from django.db.models import Q
import sweetify

from .forms import SignupForm, SigninForm, EventForm, ProfileForm, UserForm, BookEventForm, TicketForm
from .models import Event, Category, Follower, Ticket
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
                if request.user.events.count() != 0:
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
    categories = Category.objects.all()[:8]
    # events = Event.objects.all(start_date__gte = datetime.now() )
    current_events = Event.objects.filter(start_date__lte = datetime.now() , end_date__gte = datetime.now() )[:8]
    upcomming_events = Event.objects.filter(start_date__gte = datetime.now() )[:8]
    context = {
        'categories':categories,
        # 'events':events,
        'current_events':current_events,
        'upcomming_events': upcomming_events,
    }

    return render(request, 'basics/homepage.html', context)

def dashboard(request):
    events = Event.objects.filter(organizer=request.user)
    tickets = Ticket.objects.filter(user=request.user)
    context = {
        'events': events,
        'tickets':tickets,
    }
    return render(request, 'basics/dashboard.html', context)

def not_found(request, exception):
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
            sweetify.success(request, 'You successfully updated your profile', icon='success', timer=3000)
            return redirect('profile')
    context = {
        "form": form,
    }
    return render(request,'basics/profile_edit.html', context)

def user_edit(request):
    user_obj = request.user
    form = UserForm(instance=user_obj)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user_obj)
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

def organizer(request, organizer_id):
    organizer_obj = User.objects.get(id=organizer_id)
    events = Event.objects.filter(organizer=organizer_obj)
    is_follower = organizer_obj.followers.filter(follower=request.user).exists()
    context = {
        'organizer': organizer_obj,
        'is_follower': is_follower,
        'events': events,
    }
    
    return render(request, 'basics/organizer.html', context)

#####################################################################
#       event views                                                 #
#####################################################################

def event_list(request):
    events = Event.objects.all()
    query = request.GET.get('search')
    if query:
        events = events.filter(end_date__gt = datetime.now())
        events = events.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
        ).distinct()
    context = {
        "events": events,
    }
    return render(request, 'event/event_list.html', context)

def event_create(request):    
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event_obj = form.save(commit=False)
            event_obj.organizer = request.user
            event_obj.save()
            form.save_m2m()
            sweetify.success(request, 'Event created successfuly', icon='success', timer=3000)
            return redirect('event-list')
    context = {
        "form": form,
    }
    return render(request, 'event/event_create.html', context)

def event_detail(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            num_of_seats_to_book = int(form.cleaned_data['tickets'])
            # validates the num_of_seats_to_book if less than 0
            if seats_available_validate(event_obj, num_of_seats_to_book):
                # should give a message that the number of seats not available
                sweetify.warning(request, f'{num_of_seats_to_book} tickets is more than the allowed limit', button="OK", icon='warning', timer=10000)
                return redirect('event-detail', event_obj.id)
            # validates of the event is old or not
            if is_old_event(event_obj):
                sweetify.warning(request, 'this is an old event, please wait for the next one', button="OK", icon='warning', timer=10000)
                return redirect('event-detail', event_obj.id)
            ticket = form.save(commit=False)
            # decrease the number of tickets in the event
            event_obj.seats -= num_of_seats_to_book
            event_obj.save()
            # saves the ticket
            ticket.event = event_obj
            ticket.user = request.user
            ticket.save()
            # should redirect to the ticket page to print or save as pdf
            sweetify.success(request, f'{num_of_seats_to_book} Tickets to {event_obj.name} added', icon='success', timer=5000)
            return redirect('event-detail', event_obj.id)

    context = {
        'form': form,
        'event': event_obj,
        'is_old_event': is_old_event(event_obj)
    }
    return render(request, 'event/event_detail.html', context)

def event_edit(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    if not is_organizer(request, event_obj):
        sweetify.warning(request, 'You are not allowed to do this action', icon='warning', button='OK', timer=7000)
        return redirect('event-detail', event_obj.id)
    form = EventForm(instance=event_obj)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event_obj)
        if form.is_valid():
            event_obj = form.save(commit=False)
            event_obj.organizer = request.user
            event_obj.save()
            form.save_m2m()
            sweetify.success(request, 'Event successfully updated', icon='success', timer=3000)
            return redirect('event-detail', event_obj.id)
    context = {
        'form': form,
        'event': event_obj,
    }
    return render(request, 'event/event_edit.html', context)

#
# moved vent_book() to event details page
# 

def event_delete(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    event_obj.delete()
    sweetify.warning(request, 'Event successfully deleted', icon='warning', timer=3000)
    return redirect('event-list')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#       event validators                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def seats_available_validate(event, seats=0):
    if seats == 0:
        return event.seats <= 0
    return (seats - event.seats) > 0

def is_organizer(request, event_obj):
    return request.user == event_obj.organizer

def is_old_event(event_obj):
    return event_obj.end_date <= datetime.now().date()


#####################################################################
#       following views                                             #
#####################################################################

def follow(request, organizer_id):
    organizer = User.objects.get(id=organizer_id)
    Follower.objects.create(follower=request.user, following=organizer)
    sweetify.success(request, f'You now following {organizer.username}', icon='success', timer=3000)
    return redirect('organizer', organizer.id)

def unfollow(request, organizer_id):
    organizer = User.objects.get(id=organizer_id)
    Follower.objects.get(follower=request.user, following=organizer).delete()
    sweetify.warning(request, f'You unfollowed {organizer.username}', icon='warning', timer=3000)
    return redirect('organizer', organizer.id)

#####################################################################
#       ticket views                                                #
#####################################################################

def print_ticket(request, ticket_uuid):
    ticket_obj = Ticket.objects.get(number=ticket_uuid)
    if request.user != ticket_obj.user:
        sweetify.warning(request, 'You are not allowed to do this action', icon='warning', button='OK', timer=7000)
        return redirect('not_found')
    context = {
        'ticket': ticket_obj,
    }
    return render(request, 'basics/print_ticket.html', context)
