from django.db import models

class Photo(models.Model):
    date_taken = models.DateField()
    photo = models.ImageField(upload_to='photos/')
    collaborated = models.BooleanField(default=False)
    number = models.IntegerField(default=0)  # Change to IntegerField

    def __str__(self):
        return f"Photo taken on {self.date_taken}"

class Haiku(models.Model):
    number = models.AutoField(primary_key=True)
    text = models.TextField()
    author = models.CharField(max_length=100)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)  # Optional association

    def __str__(self):
        return f"Haiku {self.number} by {self.author}"
