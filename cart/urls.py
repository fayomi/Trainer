from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('add/<pk>',views.add_cart,name='add_cart'),
    path('',views.cart_detail,name='cart_detail'),
    path('cart/<pk>/remove',views.deleteItem,name='cart_remove'),


]
