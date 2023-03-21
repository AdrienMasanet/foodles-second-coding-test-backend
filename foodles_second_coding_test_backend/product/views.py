from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


class ProductsListView(APIView):
    def get(self, request):
        # Get all products in stock (stock > 0)
        products = Product.objects.filter(stock__gt=0).order_by("name")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data or {"error": "No products found"})
