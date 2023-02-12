import json
import os

import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView
from dotenv import load_dotenv

from items.models import Item

load_dotenv()


stripe.api_key = os.getenv(
    "STRIPE_SECRET_KEY", default="sk_test_4eC39HqLyjWDarjtT1zdp7dc"
)


class BuyView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        item = get_object_or_404(Item, id=item_id)
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": item.price,
                        "product_data": {
                            "name": item.name,
                            "description": item.description,
                        },
                    },
                    "quantity": 1,
                },
            ],
            metadata={"item_id": item.id},
            mode="payment",
            success_url=settings.DOMAIN + "/success/",
            cancel_url=settings.DOMAIN + "/cancel/",
        )
        return JsonResponse(
            {
                "id": session.id,
            }
        )


class ItemView(DetailView):
    model = Item
    template_name = "item.html"

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context.update(
            {
                "STRIPE_PUBLIC_KEY": os.getenv(
                    "STRIPE_PUBLIC_KEY",
                    default="pk_test_TYooMQauvdEDq54NiTphI7jx",
                ),
            }
        )
        return context


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv(
                "STRIPE_WEBHOOK_SECRET",
            ),
        )

    except ValueError as err:
        print(err)
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as err:
        print(err)
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session["customer_details"]["email"]
        send_mail(
            subject="Here is your product",
            message="Thanks for your purchase",
            recipient_list=[customer_email],
            from_email="test@test.com",
        )

    elif event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        customer_id = intent["customer"]
        customer = stripe.Customer.retrieve(customer_id)
        customer_email = customer["email"]
        send_mail(
            subject="Here is your product",
            message="Thanks for your purchase",
            recipient_list=[customer_email],
            from_email="test@test.com",
        )

    return HttpResponse(status=200)


class IntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json["email"])
            item_id = self.kwargs["pk"]
            item = Item.objects.get(id=item_id)
            intent = stripe.PaymentIntent.create(
                amount=item.price,
                currency="usd",
                customer=customer["id"],
                metadata={"item_id": item.id},
            )
            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as err:
            return JsonResponse({"error": str(err)})
