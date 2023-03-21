from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "email", "credits"]


class ClientExplicitSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source="created_at")
    updatedAt = serializers.DateTimeField(source="updated_at")

    class Meta:
        model = Client
        fields = ["id", "name", "email", "credits", "createdAt", "updatedAt"]
