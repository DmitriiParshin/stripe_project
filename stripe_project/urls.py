from django.contrib import admin
from django.urls import path

from items.views import BuyView, ItemView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/<pk>/', ItemView.as_view(), name='item'),
    path('buy/<pk>/', BuyView.as_view(), name='buy'),
]
