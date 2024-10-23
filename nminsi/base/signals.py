import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Photo

@receiver(pre_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    # Delete the file from the media folder before the Photo instance is deleted
    if instance.photo and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)
