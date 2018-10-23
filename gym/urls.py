from django.urls import path
from . import views

app_name = 'gym'
urlpatterns = [
    path('',views.TrainerListView.as_view(),name='trainer_list'),
    path('client_profile/', views.clientProfileView,name='client_profile'),
    path('trainer_profile/', views.trainerProfileView,name='trainer_profile'),
    path('client_pending/', views.clientPendingView,name='client_pending'),
    # path('profile/', views.profileView.statusChange,name='status'),
    path('trainer_register/',views.trainerRegister, name='trainer_signup'),
    path('stripe_form/',views.stripeForm, name='stripe_form'),
    path('client_register/',views.clientRegister, name='client_signup'),
    path('trainers/<pk>/',views.TrainerDetailView.as_view(),name='trainer_detail'),
    # path('create/',views.WorkoutCreateView.as_view(),name='workout_create'),
    path('update/<pk>/',views.WorkoutUpdateView.as_view(),name='workout_update'),
    path('trainers/<pk>/workout',views.addWorkout,name='addWorkout'),
    path('workout/<pk>/remove',views.deleteWorkout,name='workout_remove'),
    path('trainer/update/<pk>/',views.TrainerUpdateView.as_view(),name='trainer_update'),

]
