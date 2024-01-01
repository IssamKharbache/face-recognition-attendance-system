from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . forms import UserRegisterForm,ProfileForm,EditForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Employe
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
import os
from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse
from json import dumps






# Create your views here.
@login_required(login_url='login')
def adduser(request):
      if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request,f'User {username} added successfully you can login now')
           return redirect ('home')
      else : 
          form = UserRegisterForm()


          
      return render(request,"users/adduser.html",{'form':form})

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request,username=username,password=pass1)
        if user is not None :
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Username or password incorrect") 
    return render(request,'users/login.html')

@login_required(login_url='login')
def home(request):
    return render(request,"users/home.html")

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def addEmploye(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        fname=request.POST.get('first_name')
        messages.success(request,f'Employe {fname} added successfully')
        return redirect('allemploye') 
    context = {'form':form}
    return render(request, 'users/addemploye.html', context)



@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context ={'user_form':user_form
                     }
    #dataJSON = dumps(dataDictionary)
    return render(request, 'users/profile.html', context)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')

@login_required(login_url='login')
def editEmploye(request,pk):
    details = Employe.objects.get(cin=pk)
    form = EditForm(instance=details)
    if request.method == 'POST':
        form = EditForm(request.POST or None, request.FILES or None,instance=details)
        if form.is_valid():
            details.image.name = f'{details.cin}.jpg'
            fname=request.POST.get('first_name')
            form.save()
            messages.success(request,f'Employe {fname} updated successfully')
            return redirect('allemploye')
           
    context  = {'form':form}
    return render(request,"users/editemploye.html",context)
@login_required(login_url='login')
def allemploye(request):
    employes = Employe.objects.all()   
    context = {'employes':employes}
    return render(request,"users/allemploye.html",context)
@login_required(login_url='login')
def delete(request,pk):
    empdetails = Employe.objects.get(cin=pk)
    if request.method == "POST":
        empdetails.delete()

        return redirect('allemploye')
    context = {'Employe':empdetails}
    return render(request,"users/delete.html",context)

@login_required(login_url='login')
def aboutPage(request):
    return render(request,'users/about.html')


def editemployetry(request,pk):
    details = Employe.objects.get(cin=pk)
    form = EditForm(instance=details)
    if request.method == 'POST':
        form = EditForm(request.POST or None, request.FILES or None,instance=details)
        if form.is_valid():
            details.image.name = f'{details.cin}.jpg'

            form.save()
            fname=request.POST.get('first_name')
            messages.success(request,f'Employe {fname} updated successfully')
            return redirect('trysystem')
           
    context  = {'form':form}
    return render(request,"users/editemploye.html",context)

def deletetry(request,pk):
    empdetails = Employe.objects.get(cin=pk)
    if request.method == "POST":
        empdetails.delete()

        return redirect('trysystem')
    context = {'Employe':empdetails}
    return render(request,"users/delete.html",context)
