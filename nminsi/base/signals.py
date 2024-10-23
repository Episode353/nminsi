import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Photo, Profile
from django.contrib.auth.models import User

@receiver(pre_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    # Delete the file from the media folder before the Photo instance is deleted
    if instance.photo and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
