from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


class ProductsListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data or {"error": "No products found"})


class ProductView(APIView):
    def get(self, request, product_id):
        products = Product.objects.get(id=product_id)
        serializer = ProductSerializer(products, many=False)
        return Response(serializer.data or {"error": "No product found for id " + product_id})


# Classes below are used for testing purposes only and should not be used in production


class ProductDeleteAllView(APIView):
    def delete(self, request):
        Product.objects.all().delete()
        if Product.objects.all().count() == 0:
            return Response({"message": "All products deleted"})
        else:
            return Response({"error": "Something went wrong while deleting all products"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDeleteView(APIView):
    def delete(self, request, product_id):
        Product.objects.get(id=product_id).delete()
        if Product.objects.filter(id=product_id).count() == 0:
            return Response({"message": "Product deleted"})
        else:
            return Response({"error": "Something went wrong while deleting product"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductsSeederView(APIView):
    def post(self, request):
        Client.objects.create(
            email="client1@foodles.fr",
            credits=0,
        ).save()
        Client.objects.create(
            email="client2@foodles.fr",
            credits=10,
        ).save()
        Client.objects.create(
            email="client3@foodles.fr",
            credits=15,
        ).save()
        Client.objects.create(
            email="client4@foodles.fr",
            credits=30,
        ).save()
        Client.objects.create(
            email="client5@foodles.fr",
            credits=50,
        ).save()
        Client.objects.create(
            email="client6@foodles.fr",
            credits=70,
        ).save()
        Client.objects.create(
            email="client7@foodles.fr",
            credits=100,
        ).save()

        return Response({"message": "Clients created", "clients": Client.objects.all().values()})
