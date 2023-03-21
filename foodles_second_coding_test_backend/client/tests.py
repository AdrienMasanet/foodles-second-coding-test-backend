from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Client
from .serializers import ClientSerializer, ClientExplicitSerializer


class ClientTestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()

        # Create a test client
        self.test_client = Client.objects.create(name="Client", email="test@test.com", credits=Decimal("100.00"))

    # Model logic tests

    def test_client_create(self):
        Client.objects.create(name="Client 2", email="test2@test.com", credits=Decimal("100.00"))

        client = Client.objects.get(email="test2@test.com")

        self.assertIsNotNone(client)
        self.assertEqual(Client.objects.count(), 2)
        self.assertEqual(client.name, "Client 2")
        self.assertEqual(client.email, "test2@test.com")
        self.assertEqual(client.credits, Decimal("100.00"))

        client.delete()

    def test_client_tostring(self):
        client = Client.objects.create(name="Client 2", email="test2@test.com", credits=Decimal("100.00"))

        self.assertEqual(str(client), "test2@test.com")

        client.delete()

    # Views tests

    def test_clients_list_view(self):
        response = self.api_client.get(reverse("clients-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.test_client.id))
        self.assertEqual(response.data[0]["name"], "Client")
        self.assertEqual(response.data[0]["email"], "test@test.com")
        self.assertEqual(response.data[0]["credits"], "100.00")
        self.assertNotIn("createdAt", response.data[0])
        self.assertNotIn("updatedAt", response.data[0])

    def test_client_login_view(self):
        response = self.api_client.post(reverse("client-login"), {"id": str(self.test_client.id)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.test_client.id))
        self.assertEqual(response.data["email"], "test@test.com")
        self.assertEqual(response.data["credits"], "100.00")
        self.assertIn("createdAt", response.data)
        self.assertIn("updatedAt", response.data)
        self.assertIn("client_session_token", response.cookies)
        self.assertIsNotNone(response.cookies["client_session_token"])
