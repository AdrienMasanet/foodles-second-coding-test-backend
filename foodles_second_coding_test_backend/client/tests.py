from django.test import TestCase

from client.models import Client
from client.views import ClientsListView, ClientView, ClientsSeederView, ClientDeleteAllView, ClientDeleteView


# Tests for the client model and ORM
class ClientTestOrmCase(TestCase):
    # The clients should be created with the correct attributes
    def test_create_client(self):
        database_clients_count = Client.objects.count()

        client = Client.objects.create(
            email="client@foodles.fr",
            credits=30,
        ).save()

        self.assertEqual(Client.objects.count(), database_clients_count + 1)
        self.assertEqual(Client.objects.last().email, "client@foodles.fr")
        self.assertEqual(Client.objects.last().credits, 30)

    # The clients should be updated when edited in the database
    def test_update_client(self):
        client = Client.objects.create(
            email="client@foodles.fr",
            credits=30,
        ).save()

        client = Client.objects.last()
        client.email = "client.updated@foodles,fr"
        client.credits = 50
        client.save()

        self.assertEqual(Client.objects.last().email, "client.updated@foodles,fr")
        self.assertEqual(Client.objects.last().credits, 50)

    # The clients should be removed from the database when deleted
    def test_delete_client(self):
        client = Client.objects.create(
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
            email="client@foodles.fr",
            credits=30,
        ).save()

        response = self.client.get("/clients/")
        self.assertEqual(response.status_code, 200)

    # A client must be viewable
    def test_view_client(self):
        client = Client.objects.create(
            email="client@foodles.fr",
            credits=30,
        ).save()

        response = self.client.get("/clients/" + str(Client.objects.last().id))
        self.assertEqual(response.status_code, 200)

    # All the clients should be deleted
    def test_delete_all_clients(self):
        client = Client.objects.create(
            email="client1@foodles.fr",
            credits=30,
        ).save()

        client = Client.objects.create(
            email="client2@foodles.fr",
            credits=30,
        ).save()

        client = Client.objects.create(
            email="client3@foodles.fr",
            credits=30,
        ).save()

        response = self.client.delete("/clients/delete-all")
        self.assertEqual(response.status_code, 200)
