from django.db import models

# Create your models here.
from django.db import models

class Photo(models.Model):
    date_taken = models.DateField()
    photo = models.ImageField(upload_to='photos/')  # Adjust upload_to as needed
    collaborated = models.BooleanField(default=False)  # Indicates if the photo is grayed out

    def __str__(self):
        return f"Photo taken on {self.date_taken}"

class Haiku(models.Model):
    number = models.AutoField(primary_key=True)  # Auto-incrementing four-digit number
    text = models.TextField()  # The actual haiku text
    author = models.CharField(max_length=100)  # Author's name

    def __str__(self):
        return f"Haiku {self.number} by {self.author}"
