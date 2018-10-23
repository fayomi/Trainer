from django.shortcuts import render, redirect, get_object_or_404
from gym.models import Workout
from order.models import Order, OrderItem
from session.models import Session, AvailableSession
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings

platform_fee = 2 #aso remember to change in stripe application_fee if updated


def stripeFeeCalculator(total):
    percentage = (1.4/100) * total
    final = percentage + 0.2
    return final

def netCalculator(total, stripe_fee, platform_fee):
    net = total - stripe_fee - platform_fee
    return net



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
    client_name = request.user.clientprofile.name #newnew
    client_id = request.user.id
    client_email = request.user.email

    # to calculate the net pay
    stripe_fee = stripeFeeCalculator(total)
    service_fee = stripe_fee + platform_fee
    net_pay = netCalculator(total, stripe_fee, platform_fee)






    if request.method == 'POST':
        token = request.POST['stripeToken']
        email = request.POST['stripeEmail']
        trainer_stripe_id=cart_item.workout.trainer.stripe_id
        trainer_name = cart_item.workout.trainer.name
        description = cart_item.workout.name
        # description = cart_item.workout.name



        # customer = stripe.Customer.create(email=email,source=token)
        charge = stripe.Charge.create(amount=stripe_total,currency="gbp",description=description,source=token,application_fee=200,stripe_account=trainer_stripe_id)

        #Now Creating the Order
        try:
            order_details = Order.objects.create(
                    client_name = client_name,
                    trainer_name = trainer_name,
                    token = token,
                    total = total,
                    stripe_fee = stripe_fee,
                    platform_fee = platform_fee,
                    service_fee = service_fee,
                    net_pay = net_pay,
                    emailAddress = client_email,

            )
            order_details.save()

            for order_item in cart_items:
                oi = OrderItem.objects.create(
                        workout = order_item.workout.name,
                        sessions = order_item.workout.sessions,
                        trainer_id = order_item.workout.trainer.user.id,
                        client_id = client_id,
                        quantity = order_item.quantity,
                        price = order_item.workout.price,
                        order = order_details,
                        workout_description = order_item.workout.workout_description,

                )
                oi.save()
                # the terminal will print confirmation
                print('order has been created')

            # to get the sessions
            session_details = Session.objects.create(
                        client_id = client_id,
                        trainer_id = cart_item.workout.trainer.user.id,
                        order = order_details,
                        total_sessions = cart_item.workout.sessions,
                        workout_name = cart_item.workout.name
            )
            session_details.save()

            for available_session in cart_items:
                a_s = AvailableSession.objects.create(
                        session = session_details,
                        available_sessions = available_session.workout.sessions,
                )
                a_s.save()


            return redirect('order:thanks', order_details.id)
        except ObjectDoesNotExist:
            pass

    else:
        trainer_stripe_id = ''
        description = ''

    context = {'data_key': data_key,'description':description,'cart_items': cart_items, 'total': total,'stripe_total': stripe_total, 'counter': counter}
    return render(request,'cart/cart.html', context)



@login_required
def deleteItem(request,pk):
    cart_item = get_object_or_404(CartItem,pk=pk)
    cart_item.delete()
    return redirect('cart:cart_detail')
