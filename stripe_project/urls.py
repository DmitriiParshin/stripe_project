from django.contrib import admin
from django.urls import path

from items.views import (BuyView, CancelView, IntentView, ItemView,
                         SuccessView, stripe_webhook)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("item/<pk>/", ItemView.as_view(), name="item"),
    path("buy/<pk>/", BuyView.as_view(), name="buy"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("intent/<pk>/", IntentView.as_view(), name="intent"),
    path("webhooks/stripe/", stripe_webhook, name="stripe-webhook"),
]
