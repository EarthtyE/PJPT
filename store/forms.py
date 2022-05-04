from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    first_name=forms.CharField(max_length=100,required=True)
    
    last_name=forms.CharField(max_length=100,required=True)
    email=forms.EmailField(max_length=250,help_text='example@gmail.com')
    #phone = forms.CharField(required=True, max_length=10)
    #address = forms.CharField(max_length=1000, widget=forms.Textarea())
    #'phone','address',
    #tel=forms.CharField(max_length=10,required=True)
    #address=forms.CharField(max_length=10,required=True)

    class Meta :
        model=User
        fields=('username','first_name','last_name','email','password1','password2')
        
        