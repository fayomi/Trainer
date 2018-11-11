from django.urls import path
from . import views

app_name = 'stripe'
urlpatterns = [

    path('', views.stripe_register, name='stripe_register'),
    path('type/', views.stripe_legal_type, name='stripe_legal_type'),
    path('individual/', views.stripe_individual, name='stripe_individual'),
    path('company/', views.stripe_company, name='stripe_company'),

]
