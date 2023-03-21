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
