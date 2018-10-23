from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.http import Http404
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from .forms import TrainerSignUpForm, TrainerProfileForm,ClientSignUpForm,ClientProfileForm,WorkoutForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User,TrainerProfile, Workout, ClientProfile
from session.models import Session, AvailableSession

import requests
from django.conf import settings

CLIENT_ID = 'ca_Dht99lrMkYqjCsNZRHznzbcyhCfRzIUm'
STRIPE_TOKEN_URL = 'https://connect.stripe.com/oauth/token'
CLIENT_SECRET = settings.STRIPE_SECRET_KEY



@login_required
def clientProfileView(request):


    user_id = request.user.id

##################################### For Clients

    # this filters the most recent order
    session_filter = Session.objects.filter(client_id=user_id).order_by('-id')
    session = session_filter[0]
    session_id = session.id
    print(session.status)

    # this shows how many availbale session there are
    available = AvailableSession.objects.filter(session__id=session_id)
    for a in available:
        print(a.date)
        # print(a.available_sessions)

    # function to change status from 'available' to 'completed'
    # abstract it to if button is pressed, change status


    def statusChange():
        # print(x)
        session.status = 'completed'
        session.save()

    # this then creates a new available session

    def createAvailabeSession():
        available_session = a.available_sessions


        if session.status == 'completed' and available_session >= 1:
            available_session -= 1
            new_session = available_session


            if session.status == 'completed':
                a_s = AvailableSession.objects.create(
                        session = session,
                        available_sessions = new_session
                        )
                a_s.save()
                print(available_session)
                session.status = 'available'
                session.save()

        else:
            print('you have no more workouts')

    if (request.GET.get('use_session')):
        statusChange()
        createAvailabeSession()
        return redirect('/client_profile/') #move to pending page
    else: # probably change status to complete
        print('nothing to see here')
        pass

    context = {'session': session, 'available': available}
    return render(request,'gym/client_profile.html', context)


@login_required
def clientPendingView(request):

    return render(request, 'gym/client_pending.html')

@login_required
def trainerProfileView(request):
    user_id = request.user.id


    # this filters the most all orders
    session_filter = Session.objects.filter(trainer_id=user_id).order_by('-id')

    session_id = []
    for session in session_filter:
            session_id.append(session.id)

    print(session_id)

    available_info = []
    # for each session in the session id
    for session in session_id:
        available = AvailableSession.objects.filter(session__id=session)
        # add the number of available sessions?
        for a in available:
            print(a)
            available_info.append(a)



    context = {'session_filter': session_filter, 'available_info': available_info}
    return render(request,'gym/trainer_profile.html', context)



class TrainerListView(ListView):
    context_object_name = 'trainers'
    model = TrainerProfile

class TrainerDetailView(DetailView):
    context_object_name = 'trainer_detail'

    model = TrainerProfile
    template_name = 'gym/trainer_detail.html'





class TrainerUpdateView(LoginRequiredMixin,UpdateView):
    model = TrainerProfile
    fields = ('profile_img','skills','location','phone')

class WorkoutCreateView(LoginRequiredMixin,CreateView):

    model = Workout
    fields = ('trainer','name','price','sessions')

class WorkoutUpdateView(LoginRequiredMixin,UpdateView):
    model = Workout
    fields = ('name','price','sessions','workout_description')


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
        profile_form = TrainerProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('gym:stripe_form')
    else:
        form = TrainerSignUpForm()
        profile_form = TrainerProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request,'registration/trainer_signup_form.html', context)


def stripeForm(request):

    url = 'https://connect.stripe.com/oauth/authorize?response_type=code&client_id={}&scope=read_write'.format(CLIENT_ID)

    user = request.user

    code = request.GET.get('code')
    # print('new',code)
    data = {'client_secret': CLIENT_SECRET,'code': code,'grant_type':'authorization_code'}
    r = requests.post(STRIPE_TOKEN_URL, data=data)
    json_data =  r.json()

    try:
        id = json_data['stripe_user_id']
        user.trainerprofile.stripe_id = id
        user.trainerprofile.save()
        return redirect('/')
    except:
        pass

    context = {'url':url}
    return render(request, 'registration/stripeform.html', context)


def clientRegister(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        profile_form = ClientProfileForm(request.POST, request.FILES)

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
