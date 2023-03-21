from django.urls import path

from .views import OrdersNewView

urlpatterns = [
    path("new", OrdersNewView.as_view(), name="order-create"),
]
