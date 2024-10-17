from django.db import models

from django.db import models

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

    def __str__(self):
        return f"Photo {self.number} taken on {self.date_taken}"


class Haiku(models.Model):
    number = models.AutoField(primary_key=True)
    text = models.TextField()
    author = models.CharField(max_length=100)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)  # Optional association

    def __str__(self):
        return f"Haiku {self.number} by {self.author}"
