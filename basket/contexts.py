from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal


def basket_contents(request):
    """ Basket contents """
    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})
    for product_id, product_quantity in basket.items():
        product = get_object_or_404(Product, pk=product_id)
        total += product_quantity * product.price
        product_count += product_quantity
        basket_items.append({
            'product_id': product_id,
            'product': product,
            'quantity': product_quantity,
        })

    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
    order_total = delivery + total
    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'order_total': order_total,
    }
    return context
