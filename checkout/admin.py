from django.contrib import admin
from . models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('orderitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)
    readonly_fields = ('order_number', 'delivery_cost',
                       'total', 'order_total', 'date_ordered',
                       'original_basket', 'stripe_pid',)
    fields = ('order_number', 'user_profile', 'full_name', 'email',
              'phone_number', 'country', 'address1', 'address2', 'city',
              'county', 'postal_code', 'delivery_cost', 'total', 'order_total',
              'date_ordered', 'original_basket', 'stripe_pid',)
    list_display = ('order_number', 'full_name', 'delivery_cost', 'total',
                    'order_total', 'date_ordered',)
    ordering = ('date_ordered',)
