from django.urls import path
from . import views

app_name: 'stripe'
urlpatterns = [

    path('', views.stripe_register, name='stripe_register'),

]
