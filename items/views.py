import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, TemplateView

from items.models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY


class BuyView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = get_object_or_404(Item, id=item_id)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                'item_id': item.id
            },
            mode='payment',
            success_url=settings.DOMAIN + '/success/',
            cancel_url=settings.DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': session.id,
        })


class ItemView(DetailView):
    model = Item
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        })
        return context


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
