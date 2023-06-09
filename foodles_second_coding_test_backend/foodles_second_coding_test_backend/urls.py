from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clients/", include("client.urls")),
    path("products/", include("product.urls")),
    path("orders/", include("order.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
