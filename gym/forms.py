from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import TrainerProfile, User, ClientProfile, Workout


class TrainerSignUpForm(UserCreationForm):

    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_trainer = True
        user.email = self.cleaned_data['email']
        user.save()
        trainer = TrainerProfile.objects.create(user=user)
        return user

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ('name','description','gender','age','location','skills','profile_img')

class ClientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client= True
        user.save()
        trainer = ClientProfile.objects.create(user=user)
        return user

class ClientProfileForm(forms.ModelForm):

    class Meta:
        model = ClientProfile
        fields = ('name','goals','gender','age','location','profile_img')

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('name','price','sessions')
