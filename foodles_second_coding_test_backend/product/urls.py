from django.urls import path

from .views import ProductsListView, ProductView, ProductDeleteAllView, ProductDeleteView

urlpatterns = [
    path("", ProductsListView.as_view(), name="products-list"),
    path("delete-all", ProductDeleteAllView.as_view(), name="products-delete-all"),
    path("delete/<str:product_id>", ProductDeleteView.as_view(), name="product-delete"),
    path("<str:product_id>", ProductView.as_view(), name="product"),
]
