from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    digital = models.BooleanField(null=True)
    image = models.ImageField(default='static/images/cart_image_placeholder.png', blank=True)

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.quantity for orderitem in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.get_total for orderitem in orderitems])
        return total

    def __str__(self):
        return str(self.pk)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.address
