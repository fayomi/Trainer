from django.urls import path
from . import views

app_name = 'gym'
urlpatterns = [
    path('',views.TrainerListView.as_view(),name='trainer_list'), #to view list of trainers
    path('client/<pk>/', views.clientProfileView,name='client_profile'), # to view client profile
    path('trainer_profile/', views.trainerProfileView,name='trainer_profile'),
    path('complete/<pk>/', views.complete,name='complete'),
    path('client_pending/', views.clientPendingView,name='client_pending'),
    # path('profile/', views.profileView.statusChange,name='status'),
    path('trainer_register/',views.trainerRegister, name='trainer_signup'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    # path('stripe_form/',views.stripeForm, name='stripe_form'),
    # path('stripe_register/',views.stripeRegister, name='stripe_register'),
    path('client_register/',views.clientRegister, name='client_signup'),
    path('trainers/<pk>/',views.TrainerDetailView.as_view(),name='trainer_detail'),
    path('client/<pk>/',views.ClientDetailView.as_view(),name='client_detail'), #to update client info
    # path('create/',views.WorkoutCreateView.as_view(),name='workout_create'),
    path('update/<pk>/',views.WorkoutUpdateView.as_view(),name='workout_update'),
    path('trainers/<pk>/workout',views.addWorkout,name='addWorkout'),
    path('workout/<pk>/remove',views.deleteWorkout,name='workout_remove'),
    path('trainer/update/<pk>/',views.TrainerUpdateView.as_view(),name='trainer_update'),
    path('client/update/<pk>/',views.ClientUpdateView.as_view(),name='client_update'),

]
