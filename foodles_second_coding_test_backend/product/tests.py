import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Product
from .views import ProductsListView, ProductView, ProductsSeederView, ProductDeleteAllView, ProductDeleteView


# Get the image named "dish.jpg" in the same directory as this file so it can
# simply be used in the tests as an uploaded image
image_data = open(os.path.join(os.path.dirname(__file__), "test_images", "dish.jpg"), "rb").read()
image_file = SimpleUploadedFile(name="dish.jpg", content=image_data, content_type="image/jpeg")


# Tests for the product model and ORM
class ProductTestOrmCase(TestCase):
    # The products should be created with the correct attributes
    def test_create_product(self):
        database_products_count = Product.objects.count()

        product = Product.objects.create(
            name="product",
            price=10.00,
            description="product description",
            image=image_file,
            stock=10,
        ).save()

        product = Product.objects.last()

        self.assertEqual(Product.objects.count(), database_products_count + 1)
        self.assertEqual(product.name, "product")
        self.assertEqual(product.price, 10.00)
        self.assertEqual(product.description, "product description")
        self.assertIn("dish", product.image.name)
        self.assertIn(".jpg", product.image.name)
        self.assertEqual(product.stock, 10)

    # The products should be updated when edited in the database
    def test_update_product(self):
        product = Product.objects.create(
            name="product",
            price=10.00,
            description="product description",
            image="product_image.jpg",
            stock=10,
        ).save()

        product = Product.objects.last()
        product.name = "product updated"
        product.price = 20.00
        product.description = "product description updated"
        product.image = "product_image_updated.jpg"
        product.stock = 20
        product.save()

        modified_product = Product.objects.last()

        self.assertEqual(modified_product.name, "product updated")
        self.assertEqual(modified_product.price, 20.00)
        self.assertEqual(modified_product.description, "product description updated")
        self.assertEqual(modified_product.image, "product_image_updated.jpg")
        self.assertEqual(modified_product.stock, 20)

    # The products should be removed from the database when deleted
    def test_delete_product(self):
        product = Product.objects.create(
            name="product",
            price=10.00,
            description="product description",
            image="product_image.jpg",
            stock=10,
        ).save()

        database_products_count = Product.objects.count()

        product = Product.objects.last()
        product.delete()

        self.assertEqual(Product.objects.count(), database_products_count - 1)
