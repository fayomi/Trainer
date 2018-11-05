from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse



# This helps to seperate trainer accounts from client accounts
class User(AbstractUser):
    is_trainer = models.BooleanField(default=False)
    is_client= models.BooleanField(default=False)


class TrainerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=100,null=True)
    description = models.TextField()
    age = models.PositiveIntegerField(null=True)
    phone = models.CharField(max_length=30,null=True)
    gender = models.CharField(max_length=30,null=True)
    location = models.CharField(max_length=30,null=True)
    skills = models.CharField(max_length=30,null=True)
    profile_img = models.ImageField(upload_to='profile_image', blank=True)
    stripe_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('gym:trainer_detail', kwargs={'pk':self.pk})


class ClientProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=100,null=True)
    goals = models.CharField(max_length=30,null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=30,null=True)
    phone = models.CharField(max_length=30,null=True)
    location = models.CharField(max_length=30,null=True)
    profile_img = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('gym:client_detail', kwargs={'pk':self.pk})

class Workout(models.Model):
    trainer = models.ForeignKey(TrainerProfile,on_delete=models.CASCADE ,related_name='workouts')
    name = models.CharField(max_length=200,null=True)
    price = models.IntegerField()
    sessions = models.PositiveIntegerField(default=0)
    workout_description = models.TextField(default='There is no description available')
    subscription = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse('gym:trainer_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name
