from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from products.models import Product


def view_basket(request):
    """ A view that renders the products in the basket """
    return render(request, "basket/view_basket.html")


def add_to_basket(request, product_id):
    """ A view that gives users the ability to add products to basket"""
    product = get_object_or_404(Product, pk=product_id)
    product_quantity = int(request.POST.get('quantity'))
    redirect_url = (request.POST.get('redirect_url'))
    basket = request.session.get('basket', {})
    if product_id in list(basket.keys()):
        basket[product_id] += product_quantity
    else:
        basket[product_id] = product_quantity
    messages.success(request, "Product added to basket")
    request.session['basket'] = basket
    return redirect(redirect_url)


def update_basket(request, product_id):
    """View that allow's users to update a product quantity"""
    product = get_object_or_404(Product, pk=product_id)
    product_quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})
    if product_quantity > 0:
        basket[product_id] = product_quantity
        messages.info(request, f'Quantity updated to ({product_quantity})')
    else:
        basket.pop(product_id)
    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_product(request, product_id):
    """ A view that gives users the ability to remove products from basket"""
    try:
        product = get_object_or_404(Product, pk=product_id)
        basket = request.session.get('basket', {})
        if product_id in list(basket.keys()):
            del basket[product_id]
            messages.info(request, f'{product.name} removed from basket!')
        request.session['basket'] = basket
        return redirect(reverse('view_basket'))

    except Exception as e:
        messages.error(request, f"Error remove product {e}")
        return HttpResponse(status=500)
