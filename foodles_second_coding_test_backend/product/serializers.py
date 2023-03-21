from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, product):
        return product.image.url[1:]

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "image", "stock", "updated_at"]
