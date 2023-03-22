from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from client.models import Client
from product.models import Product
from .models import Order, OrderProduct

# Reuse image_file from the product test file
from product.tests import image_file


class OrderTestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()

        # Create a test client
        self.test_client = Client.objects.create(name="Client", email="test@test.com", credits=Decimal("100.00"))
        # Create a fake session token for the test client
        self.test_client.session_token = "fake_session_token"
        self.test_client.save()

        # Create test products
        self.test_product1 = Product.objects.create(name="Test Product 1", price=Decimal("10.00"), description="Test product 1 description", image=image_file, stock=5)
        self.test_product2 = Product.objects.create(name="Test Product 2", price=Decimal("20.57"), description="Test product 2 description", image=image_file, stock=3)
        self.test_product3 = Product.objects.create(name="Test Product 3", price=Decimal("30.00"), description="Test product 3 description", image=image_file, stock=0)
        self.test_product4 = Product.objects.create(name="Test Product 3", price=Decimal("200.00"), description="Test product 3 description", image=image_file, stock=2)

    def tearDown(self):
        Client.objects.all().delete()
        Product.objects.all().delete()

    # Model logic tests

    def test_order_create(self):
        order = Order.objects.create(client=self.test_client)

        self.assertIsNotNone(order)
        self.assertEqual(order.client, self.test_client)
        self.assertEqual(order.status, Order.OrderStatus.PENDING)
        self.assertEqual(order.total_price, Decimal("0.00"))

        order.delete()

    def test_order_tostring(self):
        order = Order.objects.create(client=self.test_client)
        OrderProduct.objects.create(order=order, product=self.test_product1, quantity=2)
        order.save()

        self.assertEqual(str(order), "test@test.com - PENDING - 20.00€")

        order.delete()

    def test_order_product_create(self):
        order = Order.objects.create(client=self.test_client)
        order_product = OrderProduct.objects.create(order=order, product=self.test_product1, quantity=2)

        self.assertEqual(order_product.order, order)
        self.assertEqual(order_product.product, self.test_product1)
        self.assertEqual(order_product.quantity, 2)

        order.delete()

    def test_calculate_total_price(self):
        order = Order.objects.create(client=self.test_client)
        OrderProduct.objects.create(order=order, product=self.test_product1, quantity=2)
        OrderProduct.objects.create(order=order, product=self.test_product2, quantity=1)
        order.save()

        self.assertEqual(order.total_price, Decimal("40.57"))

        order.delete()

    # Views tests

    def test_create_order_success(self):
        self.api_client.cookies["client_session_token"] = self.test_client.session_token
        cart_data = {str(self.test_product1.id): 2, str(self.test_product2.id): 1}
        response = self.api_client.post(reverse("order-create"), data=cart_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["clientNewCreditsAmount"]), self.test_client.credits - Decimal("40.57"))

    def test_create_order_invalid_client_session_token(self):
        self.api_client.cookies["client_session_token"] = "wrong_session_token"
        cart_data = {str(self.test_product1.id): 2, str(self.test_product2.id): 1}  # Buy 2 test_product1 and 1 test_product2
        response = self.api_client.post(reverse("order-create"), data=cart_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid client session token")

    def test_create_order_no_client_session_token(self):
        cart_data = {str(self.test_product1.id): 2, str(self.test_product2.id): 1}
        response = self.api_client.post(reverse("order-create"), data=cart_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Client session token not found")

    def test_create_order_insufficient_stock(self):
        self.api_client.cookies["client_session_token"] = self.test_client.session_token
        cart_data = {str(self.test_product1.id): 2, str(self.test_product3.id): 1}  # Test with test_product3 that has no stock
        response = self.api_client.post(reverse("order-create"), data=cart_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Available stock for product", response.data[0])

    def test_create_order_insufficient_credits(self):
        self.api_client.cookies["client_session_token"] = self.test_client.session_token
        cart_data = {str(self.test_product4.id): 1}  # Test with a product that is too expensive compared to the client credits
        response = self.api_client.post(reverse("order-create"), data=cart_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "Client credit is inferior to the order total price")
