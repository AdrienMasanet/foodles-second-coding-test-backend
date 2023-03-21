import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Client
from .serializers import ClientSerializer, ClientExplicitSerializer


class ClientsListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data or {"error": "No clients found"})


class ClientLoginView(APIView):
    def post(self, request):
        client_id = request.data.get("id")
        if client_id:
            client = Client.objects.get(id=client_id)
            if client:
                client.session_token = uuid.uuid4().hex[:255]
                client.save()
                if client.session_token:
                    response = Response(ClientExplicitSerializer(client, many=False).data)
                    response.set_cookie("client_session_token", client.session_token, max_age=None, expires=None, path="/", secure=True, httponly=True, samesite="None")
                    return response
                else:
                    return Response({"error": "Something went wrong while logging in client"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "No client found for id " + client_id}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "No id provided"}, status=status.HTTP_400_BAD_REQUEST)


class ClientLoggedInView(APIView):
    def get(self, request):
        client_session_token = request.COOKIES.get("client_session_token")
        if client_session_token:
            try:
                client = Client.objects.get(session_token=client_session_token)
            except Client.DoesNotExist:
                client = None
            if client:
                return Response(ClientExplicitSerializer(client, many=False).data)
            else:
                return Response({"error": "No client found for session token " + client_session_token}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "No session token provided"}, status=status.HTTP_400_BAD_REQUEST)


# Classes below are used for testing purposes only and should not be used in production


class ClientView(APIView):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        serializer = ClientSerializer(client, many=False)
        return Response(serializer.data or {"error": "No client found for id " + client_id}, status=status.HTTP_404_NOT_FOUND)


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
            name="Jon",
            email="jon_snow@longnight.fr",
            credits=0,
        ).save()
        Client.objects.create(
            name="Anakin",
            email="skywalker@darkside.com",
            credits=10,
        ).save()
        Client.objects.create(
            name="Qui-Gon",
            email="quigonjinn3@foodles.net",
            credits=15,
        ).save()
        Client.objects.create(
            name="Jotaro",
            email="joestar@yareyaredaze.jp",
            credits=30,
        ).save()
        Client.objects.create(
            name="Tyrion",
            email="rains.of.castamere@debpts.com",
            credits=50,
        ).save()
        Client.objects.create(
            name="Songoku",
            email="kamehameka@dragonball.jp",
            credits=22.50,
        ).save()
        Client.objects.create(
            name="Shepard",
            email="mass-effect@reaper.com",
            credits=100,
        ).save()
        Client.objects.create(
            name="Potter",
            email="harry.potter@hogwarts.en",
            credits=35,
        ).save()
        Client.objects.create(
            name="Rick",
            email="ricksanchez@multi.verse",
            credits=200,
        ).save()
        Client.objects.create(
            name="Kratos",
            email="mrkratos@gow.gr",
            credits=0,
        ).save()
        Client.objects.create(
            name="Elliot",
            email="anonymous@robot.mr",
            credits=321,
        ).save()

        return Response({"message": "Clients created", "clients": Client.objects.all().values()})
