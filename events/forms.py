from django import forms
from django.contrib.auth.models import User

from .models import Event, Profile, Ticket

#####################################################################
#       auth forms                                                  #
#####################################################################

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password', 'email']
        
        widgets={
            'password': forms.PasswordInput(),
        }

class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'location', 'birthdate']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','password', ]


#####################################################################
#       event forms                                                 #
#####################################################################

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']
        
        widgets = {
        	'start_date': forms.DateInput(attrs={'type':'date'}),
        	'end_date': forms.DateInput(attrs={'type':'date'}),
        }

class BookEventForm(forms.Form):
    seats = forms.IntegerField(required=True, max_value=10, min_value=1)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['tickets']

