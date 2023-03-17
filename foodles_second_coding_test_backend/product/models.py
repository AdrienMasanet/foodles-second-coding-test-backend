import uuid
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.files.storage import default_storage
from django.conf import settings


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images/")
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=Product)
# Delete image from storage when product is deleted to prevent orphaned images
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        image_path = str(instance.image)
        full_path = f"{settings.MEDIA_ROOT}/{image_path}"
        default_storage.delete(full_path)