from django.urls import path

from .views import ClientsListView, ClientLoginView, ClientLoggedInView, ClientView, ClientsSeederView, ClientDeleteAllView, ClientDeleteView

urlpatterns = [
    path("", ClientsListView.as_view(), name="clients-list"),
    path("login", ClientLoginView.as_view(), name="client-login"),
    path("loggedin", ClientLoggedInView.as_view(), name="client-loggedin"),
    path("seeder", ClientsSeederView.as_view(), name="clients-seeder"),
    path("delete-all", ClientDeleteAllView.as_view(), name="clients-delete-all"),
    path("delete/<str:client_id>", ClientDeleteView.as_view(), name="client-delete"),
    path("<str:client_id>", ClientView.as_view(), name="client"),
]
