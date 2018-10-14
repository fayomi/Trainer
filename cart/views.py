from django.shortcuts import render, redirect, get_object_or_404
from gym.models import Workout
from order.models import Order, OrderItem
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings


# Create your views here.
@login_required
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart

@login_required
def add_cart(request, pk):
    workout = Workout.objects.get(pk=pk)
    trainer = workout.trainer.name # new addition
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(workout=workout,trainer=trainer,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(workout = workout,trainer=trainer,quantity = 1,cart = cart)
        cart_item.save()
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request, total=0, counter=0, cart_items = None):

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.workout.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass



    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = total * 100
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    name = request.user.clientprofile.name #newnew




    if request.method == 'POST':
        token = request.POST['stripeToken']
        email = request.POST['stripeEmail']
        trainer_id=cart_item.workout.trainer.stripe_id
        description = cart_item.workout.name
        # description = cart_item.workout.name



        # customer = stripe.Customer.create(email=email,source=token)
        charge = stripe.Charge.create(amount=stripe_total,currency="gbp",description=description,source=token,application_fee=300,stripe_account=trainer_id)

        #Now Creating the Order
        try:
            order_details = Order.objects.create(
                    name = name, #newnew
                    token = token,
                    total = total,
                    emailAddress = email,

            )
            order_details.save()

            for order_item in cart_items:
                oi = OrderItem.objects.create(
                        workout = order_item.workout.name,
                        trainer = order_item.workout.trainer.name,
                        quantity = order_item.quantity,
                        price = order_item.workout.price,
                        order = order_details

                )
                oi.save()
                # the terminal will print confirmation
                print('order has been created')

            return redirect('order:thanks', order_details.id)
        except ObjectDoesNotExist:
            pass

    else:
        trainer_id = ''
        description = ''

    context = {'data_key': data_key,'description':description,'cart_items': cart_items, 'total': total,'stripe_total': stripe_total, 'counter': counter}
    return render(request,'cart/cart.html', context)



@login_required
def deleteItem(request,pk):
    cart_item = get_object_or_404(CartItem,pk=pk)
    cart_item.delete()
    return redirect('cart:cart_detail')
