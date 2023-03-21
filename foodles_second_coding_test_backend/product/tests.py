import os
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Product
from .serializers import ProductSerializer

# Get the image named "dish.jpg" in the same directory as this file so it can
# simply be used in the tests as an uploaded image
image_data = open(os.path.join(os.path.dirname(__file__), "test_images", "dish.jpg"), "rb").read()
image_file = SimpleUploadedFile(name="dish.jpg", content=image_data, content_type="image/jpeg")


class ProductTestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()

        # Create a test product
        self.test_product = Product.objects.create(name="Test Product", price=9.99, description="Test product description", image=image_file, stock=5)

    # Model logic tests

    def test_product_create(self):
        Product.objects.create(name="Test Product 2", price=9.99, description="Test product 2 description", image=image_file, stock=5)

        product = Product.objects.get(name="Test Product 2")

        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Test Product 2")
        self.assertEqual(product.price, Decimal("9.99"))
        self.assertEqual(product.description, "Test product 2 description")
        self.assertEqual(product.stock, 5)

        product.delete()

    def test_product_tostring(self):
        product = Product.objects.create(name="Test Product 2", price=9.99, description="Test product 2 description", image=image_file, stock=5)

        self.assertEqual(str(product), "Test Product 2")

        product.delete()

    def test_product_image_delete(self):
        # Create a second product with the same image
        product = Product.objects.create(name="Test Product 2", price=19.99, description="Test product 2 description", image=image_file, stock=3)
        # Delete the first product
        self.test_product.delete()

        self.assertFalse(os.path.exists(self.test_product.image.path))  # Check if the image file of the first product is deleted
        self.assertTrue(os.path.exists(product.image.path))  # Check if the image file still exists for the new product

        product.delete()

    def test_product_image_update(self):
        # Save the initial image path
        initial_image_path = self.test_product.image.path

        # Update the product image
        new_image_data = open(os.path.join(os.path.dirname(__file__), "test_images", "dish.jpg"), "rb").read()
        new_image_file = SimpleUploadedFile(name="dish.jpg", content=new_image_data, content_type="image/jpeg")
        self.test_product.image = new_image_file
        self.test_product.save()

        # Check if the initial image file is deleted
        self.assertFalse(os.path.exists(initial_image_path))

        # Check if the new image file exists
        self.assertTrue(os.path.exists(self.test_product.image.path))

        # Clean up
        self.test_product.delete()

    # Views tests

    def test_products_list_view(self):
        url = reverse("products-list")
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        products = Product.objects.filter(stock__gt=0)
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(response.data, serializer.data)
