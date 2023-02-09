from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

#Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate

#Forms and Models
from .models import Profile
from .forms import ProfileForm,SignUpForm

#Messages
from django.contrib import messages

# Create your views here.
def sign_up(request):
    form = SignUpForm()
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Successfully!")
            return HttpResponseRedirect(reverse('login_app:login'))
    diction = {'form':form}
    return render(request,'login_app/signup.html',context=diction)

def login_user(request):
    form = AuthenticationForm()
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            credentials = form.clean()
            #Bohubrihi - username = form.cleaned_data.get('username')
            #Bohubrihi - password = form.cleaned_data.get('password')
            user = authenticate(username=credentials['username'],password=credentials['password'])
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('shop_app:home'))
    diction = {'form':form}
    return render(request,'login_app/login.html',context=diction)

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are logged out!!")
    return HttpResponseRedirect(reverse('shop_app:home'))

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method=='POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated!!")
            form = ProfileForm(instance=profile)
    diction = {'form':form}
    return render(request,'login_app/changeprofile.html',context=diction)
