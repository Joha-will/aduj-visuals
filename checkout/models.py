from django.db import models


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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False,
                              blank=False, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,
                                blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    orderitem_total = models.DecimalField(max_digits=8, decimal_places=2,
                                          null=False, blank=False,
                                          editable=False)