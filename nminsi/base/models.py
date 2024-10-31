from django.db import models
import os
from django.conf import settings

class Photo(models.Model):
    date_taken = models.DateField()
    photo = models.ImageField(upload_to='photos/')
    collaborated = models.BooleanField(default=False)
    number = models.IntegerField(default=0)  # Matches the "#" from the spreadsheet
    discard = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    wbord = models.BooleanField(default=False)
    insta = models.BooleanField(default=False)
    x = models.BooleanField(default=False)
    folder = models.BooleanField(default=False)
    gallery = models.BooleanField(default=False)
    photographer = models.CharField(max_length=100, default='N. Minsi')
    queued = models.BooleanField(default=False)  # New field for queued status
    posted = models.BooleanField(default=False)  # New field for posted status
    authentication = models.TextField(blank=True, null=True)  # New text field for user input

    def __str__(self):
        return f"Photo {self.number} taken on {self.date_taken}"

    def delete(self, *args, **kwargs):
        # First delete the photo file from the media folder
        if self.photo and os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        # Call the parent class delete method to delete the object from the database
        super().delete(*args, **kwargs)

        # First delete the photo file from the media folder
        if self.photo and os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        # Call the parent class delete method to delete the object from the database
        super().delete(*args, **kwargs)


class Haiku(models.Model):
    number = models.AutoField(primary_key=True)
    text = models.TextField()
    author = models.CharField(max_length=100)
    instagram_tag = models.CharField(max_length=255, blank=True, null=True)  # New field for Instagram tag or URL
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)

    def get_instagram_link(self):
        if self.instagram_tag:  # Check if instagram_tag is not None or empty
            if self.instagram_tag.startswith('http'):
                return self.instagram_tag  # If it's a full link
            return f"https://www.instagram.com/{self.instagram_tag.lstrip('@')}/"  # If it's a username
        return None  # Or return a default value or raise an exception if needed

    def __str__(self):
        return self.text

    
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instagram_handle = models.CharField(max_length=100, blank=True, null=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
