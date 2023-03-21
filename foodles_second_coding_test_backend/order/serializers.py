from rest_framework import serializers

from .models import Order, OrderProduct
from client.models import Client
from product.models import Product
from client.serializers import ClientSerializer
from product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "client", "products", "status", "total_price", "created_at", "updated_at"]

    def create(self, validated_data):
        # Get the client id and cart data from the context
        client_id = self.context.get("client_id")
        cart_data = self.context.get("cart_data")

        try:
            # Get the client in database
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            # If client is not found, raise an error
            raise serializers.ValidationError("Client not found")

        # Create and save the order in the database for this client
        order = Order.objects.create(client=client)
        order.status = "PENDING"
        order.save()

        # Add all products to the order
        for product_id, quantity in cart_data.items():
            product = Product.objects.get(id=product_id)

            # If product is not found, delete the order and raise an error
            if not product:
                order.delete()
                raise serializers.ValidationError("Product not found for id " + product_id)

            # If product stock is inferior to the order quantity, delete the order and raise an error
            if product.stock < quantity:
                order.delete()
                raise serializers.ValidationError("Available stock for product " + product_id + " is strictly inferior to the order quantity")

            # Create and save a OrderProduct in the database with the affiliate order, product and quantity
            order_product = OrderProduct(order=order, product=product, quantity=quantity)
            order_product.save()

        # Save the order to update the total price depending on the products freshly added
        order.save()

        # Check if the total price of the order is inferior or equal to the client's credit
        if order.total_price > client.credits:
            # If not, delete the order and raise an error
            order.status = "CANCELED"
            order.save()
            raise serializers.ValidationError("Client credit is inferior to the order total price")

        # Substract the total price of the order to the client's credit
        client.credits -= order.total_price
        client.save()

        # Substract the quantity of each product from the product's stock
        for product_id, quantity in cart_data.items():
            product = Product.objects.get(id=product_id)
            product.stock -= quantity
            product.save()

        # Set status from PENDING to PAID and save the order
        order.status = "PAID"
        order.save()
        return client.credits
