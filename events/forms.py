from django import forms
from django.contrib.auth.models import User

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
