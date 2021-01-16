from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


# Create your views here.

def store(request):
    products = Product.objects.all()

    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    cart_items = order.get_cart_items
    print(cart_items)
    context = {
        'products': products,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    products = Product.objects.first()

    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    cart_items = order.get_cart_items
    orderitems = order.orderitem_set.all()

    context = {
        'products': products,
        'order': order,
        'orderitems': orderitems,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {

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
        orderItem.quantity = orderItem.quantity + 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item Updated!", safe=False)
