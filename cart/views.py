from django.shortcuts import render, redirect, get_object_or_404
from gym.models import Workout
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required



# Create your views here.
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, pk):
    workout = Workout.objects.get(pk=pk)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(workout=workout,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(workout = workout,quantity = 1,cart = cart)
        cart_item.save()
    return redirect('cart:cart_detail')

def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.workout.price * cart_item.quantity)
            counter += cart_item.quantity
            stripe_total = total * 100
    except ObjectDoesNotExist:
        pass

    context = {'cart_items': cart_items, 'total': total,'stripe_total': stripe_total, 'counter': counter}
    return render(request,'cart/cart.html', context)



@login_required
def deleteItem(request,pk):
    cart_item = get_object_or_404(CartItem,pk=pk)
    cart_item.delete()
    return redirect('cart:cart_detail')
