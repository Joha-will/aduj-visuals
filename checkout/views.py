from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from .forms import OrderForm
from django.conf import settings
from basket.contexts import basket_contents

import stripe


def checkout(request):

    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, " There's nothing in your basket!")
        return redirect(reverse('products'))
    current_basket = basket_contents(request)
    total_amount = current_basket['order_total']
    stripe_total = round(total_amount * 100)
