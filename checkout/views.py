from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from django.views.decorators.http import require_POST
from .forms import OrderForm, Order
from .models import OrderItem
from products.models import Product
from django.contrib import messages
from django.conf import settings
from basket.contexts import basket_contents
from profile_management.models import UserProfile
from profile_management.forms import UserProfileForm
import json
import stripe


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_details': request.POST.get('save_details'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, "We're sorry, your payment could not\
            be processed, please try again later.")
        return HttpResponse(content=e, status=400)


def checkout(request):
    """ A view that renders the checkout page """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        basket = request.session.get('basket', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address1': request.POST['address1'],
            'address2': request.POST['address2'],
            'city': request.POST['city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'postal_code': request.POST['postal_code'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.strip_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
            for product_id, product_quantity in basket.items():
                try:
                    product = get_object_or_404(Product, id=product_id)
                    if isinstance(product_quantity, int):
                        order_item = OrderItem(
                            order=order,
                            quantity=product_quantity,
                            product=product,
                        )
                        order_item.save()
                except Product.DoesNotExist:
                    messages.error(request, " We're Sorry! One of the product \
                         in your basket was not found in our database, please \
                        contact for help!")
                    order.delete()
                    return redirect(reverse('view_basket'))
            request.session['save-details'] = 'save-details' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, "There was an error when submiting the\
             form. Please check the details you have provided. ")
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, " There's nothing in your basket!")
            return redirect(reverse('products'))
        current_basket = basket_contents(request)
        total_amount = current_basket['order_total']
        stripe_total = round(total_amount * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_country,
                    'postal_code': profile.default_postal_code,
                    'city': profile.default_city,
                    'address1': profile.default_address1,
                    'address2': profile.default_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()
    if not stripe_public_key:
        messages.warning(request, "Stripe Public key missing, did you forget \
             to set variable?")
    context = {
        'order_form':  order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """ This view is used for successful checkouts"""
    save_details = request.session.get('save-details')
    order = get_object_or_404(Order, order_number=order_number)
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()
    if save_details:
        profile_details = {
            'default_phone_number': order.phone_number,
            'default_country': order.country,
            'default_postal_code': order.postal_code,
            'default_city': order.city,
            'default_address1': order.address1,
            'default_address2': order.address2,
            'default_county': order.county,
        }
        user_profile_form = UserProfileForm(profile_details, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
    messages.info(request, f"Thank you for ordering. We received your order \
         and will begin processing it soon. Your order no. {order_number}. A \
            confirmation email will be sent to {order.email}.")
    if 'basket' in request.session:
        del request.session['basket']
    context = {
        'order': order,
    }
    return render(request, 'checkout/checkout_success.html', context)
