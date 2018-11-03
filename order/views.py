from django.shortcuts import render,get_object_or_404
from .models import Order, OrderItem
from session.models import Session, AvailableSession
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def thanks(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)

    context = {'customer_order': customer_order}
    return render(request, 'order/thanks.html', context)

#client order history
@login_required
def orderHistory(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(client_email=email)

    context = {'order_details': order_details}
    return render(request,'order/orders_list.html',context)

@login_required
def viewOrder(request, order_id):
    # user_id = request.user.id

    if request.user.is_authenticated:
        email = str(request.user.email)
        order = Order.objects.get(id=order_id,client_email=email)
        order_items = OrderItem.objects.filter(order=order)

    session = Session.objects.get(order_id=order_id)
    session_id = session.id

    available = AvailableSession.objects.filter(session__id=session_id)

    # total gives hw many sessions they start with
    total = available[0].available_sessions





    context = {'order': order, 'order_items': order_items, 'available': available, 'total': total}
    return render(request, 'order/order_detail.html', context)


#trainer order history
@login_required
def trainerOrderHistory(request):
    if request.user.is_authenticated:
        trainer_id = str(request.user.id)
        trainer_orders = OrderItem.objects.filter(trainer_id=trainer_id)
        print(trainer_orders)

    context = {'trainer_orders':trainer_orders}
    return render(request,'order/trainer_orders_list.html',context)
