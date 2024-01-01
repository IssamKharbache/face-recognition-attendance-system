from django import forms
from .models import *
from django.core.validators import EmailValidator

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta :
        model = User
        fields = ['username','email','password1','password2']
    
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'Username here',
            'class':'form-control',
            'style':'font-family:arial;'
        }
    ))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder':'Example@gmail.com',
            'class':'form-control '
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Enter your password',
            'class':'form-control'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Confirm your password',
            'class':'form-control'
        }
    ))
    
    
    

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['first_name','last_name','cin','date','phone','email','profession','image','timein','timeout','timeworked']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['cin'].widget.attrs['class'] = 'form-control'
        
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['profession'].widget.attrs['class'] = 'form-control' 
        
    date =forms.DateField(widget=forms.DateInput(
        attrs={
            'class':'form-control',
            'type':'date'
            
        }
    ))
    timein = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'value':'2023-01-01 00:00:00'
            
        }
    ))
    timeout = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'value':'2023-01-01 00:00:00'
                 
           
        }
    ))
    timeworked = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'value':'0'  
        }
    ))
    
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class':'form-control',
             'id':'file',
             
        
        }
    ))


class EditForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['first_name','last_name','cin','date','phone','email','profession','image','timein','timeout','timeworked']

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['profession'].widget.attrs['class'] = 'form-control'
        self.fields['cin'].widget.attrs['class'] = 'form-control'
        self.fields['cin'].widget.attrs['readonly'] = True 
 

    timein = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'value':'2023-01-01 00:00:00'
            
        }
    ))
    timeout = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'value':'2023-01-01 00:00:00'
                 
           
        }
    ))
    timeworked = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'value':'0'  
        }
    ))
    
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class':'form-control',
        
        }
    ))

    date =forms.DateField(widget=forms.DateInput(
        attrs={
            'class':'form-control',
            'type':'date'
            
        }
    )) 

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name= forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

