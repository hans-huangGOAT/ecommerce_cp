from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import *


# Create your views here.

def store(request):
    products = Product.objects.all()
    data = cartData(request)
    order = data['order']
    cart_items = data['cart_items']
    orderitems = data['orderitems']
    context = {
        'products': products,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    order = data['order']
    cart_items = data['cart_items']
    orderitems = data['orderitems']
    context = {
        'order': order,
        'orderitems': orderitems,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    order = data['order']
    cart_items = data['cart_items']
    orderitems = data['orderitems']
    context = {
        'order': order,
        'orderitems': orderitems,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    product = Product.objects.get(id=product_id)

    orderItem, created = OrderItem.objects.get_or_create(product=product, order=order)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item Updated!", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(data, request)

    total = data['form']['total']
    order.transaction_id = transaction_id

    print(total, "   ", order.get_cart_total)
    if total == str(order.get_cart_total):
        print("Fuck")
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)
