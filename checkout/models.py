from django.db import models

import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum
from products.models import Product


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=254, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=30, null=False, blank=False)
    address1 = models.CharField(max_length=254, null=False, blank=False)
    address2 = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=254, null=False, blank=False)
    county = models.CharField(max_length=254, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=8, decimal_places=2,
                                        null=False, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                                default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def generate_order_number(self):
        """ Random number generator for unique order number using UUID. """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Updates order total each time a
        order item is added,to account for delivery costs.
        """
        self.total = self.orderitems.aggregate(Sum('orderitem_total'))[
                                            'orderitem_total__sum'] or 0
        sdp = settings.STANDARD_DELIVERY_PERCENTAGE
        self.delivery_cost = self.total * sdp / 100
        self.order_total = self.total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Overrides the original save method to set the
        order number if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False,
                              blank=False, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,
                                blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    orderitem_total = models.DecimalField(max_digits=8, decimal_places=2,
                                          null=False, blank=False,
                                          editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set
        the orderitem total and update the other total.
        """
        self.orderitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Order Item # ' + str(self.order.order_number) + ' with '\
         + str(self.product.name)
