from django.urls import path

from .views import OrdersListView, OrdersNewView, OrderView, OrderDeleteAllView, OrderDeleteView

urlpatterns = [
    path("", OrdersListView.as_view(), name="orders-list"),
    path("new", OrdersNewView.as_view(), name="order-create"),
    path("delete-all", OrderDeleteAllView.as_view(), name="orders-delete-all"),
    path("delete/<str:order_id>", OrderDeleteView.as_view(), name="order-delete"),
    path("<str:order_id>", OrderView.as_view(), name="order"),
]
