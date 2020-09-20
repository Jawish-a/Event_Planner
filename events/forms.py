from django import forms
from django.contrib.auth.models import User

from .models import Event

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


#####################################################################
#       event forms                                                 #
#####################################################################

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        
        widgets = {
        	'start_date': forms.DateInput(attrs={'type':'date'}),
        	'end_date': forms.DateInput(attrs={'type':'date'}),
        }
