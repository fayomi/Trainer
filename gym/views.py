from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from .forms import TrainerSignUpForm, TrainerProfileForm,ClientSignUpForm,ClientProfileForm,WorkoutForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User,TrainerProfile, Workout, ClientProfile




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





class TrainerUpdateView(LoginRequiredMixin,UpdateView):
    model = TrainerProfile
    fields = ('profile_img','skills','location')

class WorkoutCreateView(LoginRequiredMixin,CreateView):

    model = Workout
    fields = ('trainer','name','price')

class WorkoutUpdateView(LoginRequiredMixin,UpdateView):
    model = Workout
    fields = ('name','price')


@login_required
def addWorkout(request,pk):
    trainerProfile = get_object_or_404(TrainerProfile,pk=pk)
    trainer_pk = trainerProfile.pk
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.trainer = trainerProfile
            workout.save()
            return redirect('gym:trainer_detail',pk=trainer_pk)
    else:
        form = WorkoutForm()

    context = {'form':form}

    return render(request,'gym/workout_form.html',context)

@login_required
def deleteWorkout(request,pk):
    workout = get_object_or_404(Workout,pk=pk)
    trainer_pk = workout.trainer.pk
    workout.delete()
    return redirect('gym:trainer_detail',pk=trainer_pk)





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
