from django.shortcuts import get_object_or_404, HttpResponse


class StripeWH_Handler:
    """ Handle's Stripe webhooks"""
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle's all generic/unknown/unexpected webhook event """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)