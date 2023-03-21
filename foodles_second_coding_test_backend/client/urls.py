from django.urls import path

from .views import ClientsListView, ClientLoginView, ClientLoggedInView, ClientsSeederView

urlpatterns = [
    path("", ClientsListView.as_view(), name="clients-list"),
    path("login", ClientLoginView.as_view(), name="client-login"),
    path("loggedin", ClientLoggedInView.as_view(), name="client-loggedin"),
    path("seeder", ClientsSeederView.as_view(), name="clients-seeder"),
]
