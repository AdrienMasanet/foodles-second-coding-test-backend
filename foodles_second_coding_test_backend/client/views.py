from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from client.models import Client
from client.serializers import ClientSerializer


class ClientsListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data or {"error": "No clients found"})


class ClientView(APIView):
    def get(self, request, client_id):
        return Response(Client.objects.filter(id=client_id).values() or {"error": "No clients found"})


# Classes below are used for testing purposes only and should not be used in production


class ClientDeleteAllView(APIView):
    def delete(self, request):
        Client.objects.all().delete()
        return Response({"message": "All clients deleted"})


class ClientDeleteView(APIView):
    def delete(self, request, client_id):
        Client.objects.filter(id=client_id).delete()
        return Response({"message": "Client deleted"})


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
