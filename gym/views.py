from django.shortcuts import render, redirect
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from .forms import TrainerSignUpForm, TrainerProfileForm,ClientSignUpForm,ClientProfileForm
from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User,TrainerProfile, Workout



# Create your views here.
# @login_required
class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'gym/profile.html'

class TrainerListView(ListView):
    context_object_name = 'trainers'
    model = TrainerProfile

class TrainerDetailView(DetailView):
    context_object_name = 'trainer_detail'
    model = TrainerProfile
    template_name = 'gym/trainer_detail.html'


def trainerRegister(request):
    if request.method == 'POST':
        form = TrainerSignUpForm(request.POST)
        profile_form = TrainerProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('/')
    else:
        form = TrainerSignUpForm()
        profile_form = TrainerProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request,'registration/trainer_signup_form.html', context)


def clientRegister(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        profile_form = ClientProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('/')
    else:
        form = ClientSignUpForm()
        profile_form = ClientProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request,'registration/client_signup_form.html', context)
