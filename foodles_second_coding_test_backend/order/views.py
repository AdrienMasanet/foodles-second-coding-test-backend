from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from client.models import Client
from .serializers import OrderSerializer


class OrdersNewView(APIView):
    def post(self, request):
        client_session_token = request.COOKIES.get("client_session_token")
        if client_session_token:
            try:
                client = Client.objects.get(session_token=client_session_token)
            except Client.DoesNotExist:
                client = None
            if client:
                # If a client was found with the session token, get the cart data from the request
                cart_data = request.data

                # Call the serializer to handle the logic of creating the order object and adding the products to it
                serializer = OrderSerializer(context={"client_id": client.id, "cart_data": cart_data}, data={})
                if serializer.is_valid():
                    # If the serializer is valid, save the order and return the client'n new credits
                    clientNewCreditsAmount = serializer.save()
                    return Response({"clientNewCreditsAmount": clientNewCreditsAmount})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid client session token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Client session token not found"}, status=status.HTTP_401_UNAUTHORIZED)


# Classes below are used for testing purposes only and should not be used in production


class OrdersListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data or {"error": "No orders found"})


class OrderView(APIView):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data or {"error": "No order found for id " + order_id})


class OrderDeleteAllView(APIView):
    def delete(self, request):
        Order.objects.all().delete()
        if Order.objects.all().count() == 0:
            return Response({"message": "All orders deleted"})
        else:
            return Response({"error": "Something went wrong while deleting all orders"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDeleteView(APIView):
    def delete(self, request, order_id):
        Order.objects.get(id=order_id).delete()
        if Order.objects.filter(id=order_id).count() == 0:
            return Response({"message": "Order deleted"})
        else:
            return Response({"error": "Something went wrong while deleting order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
