from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Client
from .serializers import ClientSerializer


class ClientsListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data or {"error": "No clients found"})


class ClientView(APIView):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        serializer = ClientSerializer(client, many=False)
        return Response(serializer.data or {"error": "No client found for id " + client_id})


# Classes below are used for testing purposes only and should not be used in production


class ClientDeleteAllView(APIView):
    def delete(self, request):
        Client.objects.all().delete()
        if Client.objects.all().count() == 0:
            return Response({"message": "All clients deleted"})
        else:
            return Response({"error": "Something went wrong while deleting all clients"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientDeleteView(APIView):
    def delete(self, request, client_id):
        Client.objects.get(id=client_id).delete()
        if Client.objects.filter(id=client_id).count() == 0:
            return Response({"message": "Client deleted"})
        else:
            return Response({"error": "Something went wrong while deleting client"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientsSeederView(APIView):
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
