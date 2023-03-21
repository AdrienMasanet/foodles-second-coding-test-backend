from django.test import TestCase

from .models import Client
from .views import ClientsListView, ClientView, ClientsSeederView, ClientDeleteAllView, ClientDeleteView


# Tests for the client model and ORM
class ClientTestOrmCase(TestCase):
    # The clients should be created with the correct attributes
    def test_create_client(self):
        database_clients_count = Client.objects.count()

        client = Client.objects.create(
            name="Client",
            email="client@foodles.fr",
            credits=30,
        ).save()

        client = Client.objects.last()

        self.assertEqual(Client.objects.count(), database_clients_count + 1)
        self.assertEqual(client.name, "Client")
        self.assertEqual(client.email, "client@foodles.fr")
        self.assertEqual(client.credits, 30)

    # The clients should be updated when edited in the database
    def test_update_client(self):
        client = Client.objects.create(
            name="Client",
            email="client@foodles.fr",
            credits=30,
        ).save()

        client = Client.objects.last()
        client.name = "Client"
        client.email = "client.updated@foodles,fr"
        client.credits = 50
        client.save()

        modified_client = Client.objects.last()

        self.assertEqual(modified_client.name, "Client")
        self.assertEqual(modified_client.email, "client.updated@foodles,fr")
        self.assertEqual(modified_client.credits, 50)

    # The clients should be removed from the database when deleted
    def test_delete_client(self):
        client = Client.objects.create(
            name="Client",
            email="client@foodles.fr",
            credits=30,
        ).save()

        database_clients_count = Client.objects.count()

        client = Client.objects.last()
        client.delete()

        self.assertEqual(Client.objects.count(), database_clients_count - 1)


# Tests for the client views
class ClientTestViewCase(TestCase):
    # The clients should be listed
    def test_list_clients(self):
        client = Client.objects.create(
            name="Client",
            email="client@foodles.fr",
            credits=30,
        ).save()

        response = self.client.get("/clients/")
        self.assertEqual(response.status_code, 200)

    # A client must be viewable
    def test_view_client(self):
        client = Client.objects.create(
            name="Client",
            email="client@foodles.fr",
            credits=30,
        ).save()

        response = self.client.get("/clients/" + str(Client.objects.last().id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(Client.objects.last().id))

    # All the clients should be deleted
    def test_delete_all_clients(self):
        response = self.client.delete("/clients/delete-all")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Client.objects.count(), 0)
