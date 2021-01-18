import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        print("Cart: ", cart)
    except:
        cart = {}
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']
    orderitems = []

    for i in cart:
        try:
            cart_items += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            orderitems.append(item)

            if not product.digital:
                order['shipping'] = True

        except:
            pass

    return {
        'order': order,
        'orderitems': orderitems,
        'cart_items': cart_items,
    }


def cartData(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
        cart_items = order.get_cart_items
        orderitems = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        cart_items = cookieData['cart_items']
        orderitems = cookieData['orderitems']
    return {
        'order': order,
        'orderitems': orderitems,
        'cart_items': cart_items,
    }

def guestOrder(data, request):
    print('User is not logged in')

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['orderitems']

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order
