from django.shortcuts import get_object_or_404, HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from products.models import Product
from .models import Order, OrderItem
from profile_management.models import UserProfile
from django.core.mail import send_mail

import time
import json
import stripe


class StripeWH_Handler:
    """ Handle's Stripe webhooks"""
    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """ This method sends the user a confirmation email"""
        user_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user_email]
        )

    def handle_event(self, event):
        """ Handle's all generic/unknown/unexpected webhook event """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ Handle's the payment_intent.success webhook from stripe """
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_details = intent.metadata.save_details
        # Get Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        order_total = round(stripe_charge.amount / 100, 2)
        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        # Users profile will be updated if save_details is checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_details:
                profile.default_phone_number = shipping_details.phone,
                profile.default_country = shipping_details.address.country,
                profile.default_address1 = shipping_details.address.line1,
                profile.default_address2 = shipping_details.address.line2,
                profile.default_city = shipping_details.address.city,
                profile.default_county = shipping_details.address.state,
                profile.default_postal_code = shipping_details.address.postal_code,  # noqa
                profile.save()
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    address1__iexact=shipping_details.address.line1,
                    address2__iexact=shipping_details.address.line2,
                    city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    postal_code__iexact=shipping_details.address.postal_code,
                    order_total=order_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
            if order_exists:
                self._send_confirmation_email(order)
                print(intent)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]}\
                        | SUCCESS: Verified order already in database',
                    status=200)
            else:
                order = None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        user_profile=profile,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.address.country,
                        address1=shipping_details.address.line1,
                        address2=shipping_details.address.line2,
                        city=shipping_details.address.city,
                        county=shipping_details.address.state,
                        postal_code=shipping_details.address.postal_code,
                        original_basket=basket,
                        stripe_pid=pid,
                    )
                    for product_id, product_quantity in json.loads(basket).items():  # noqa
                        product = Product.objects.get(id=product_id)
                        if isinstance(product_quantity, int):
                            order_item = OrderItem(
                                order=order,
                                quantity=product_quantity,
                                product=product,
                            )
                            order_item.save()
                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(content=f'Webhook received: \
                        {event["type"]}| ERROR: {e}', status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS:\
                 Created order in webhook', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle's the payment_intent.failed webhook from stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
