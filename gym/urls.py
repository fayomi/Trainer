from django.urls import path
from . import views

app_name = 'gym'
urlpatterns = [
    path('',views.TrainerListView.as_view(),name='trainer_list'),
    path('profile/', views.ProfileView.as_view(),name='profile'),
    path('trainer_register/',views.trainerRegister, name='trainer_signup'),
    path('client_register/',views.clientRegister, name='client_signup'),
    path('trainers/<pk>/',views.TrainerDetailView.as_view(),name='trainer_detail'),
    path('create/',views.WorkoutCreateView.as_view(),name='workout_create'),
    path('update/<pk>/',views.WorkoutUpdateView.as_view(),name='workout_update'),

]
