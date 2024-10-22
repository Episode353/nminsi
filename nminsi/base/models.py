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
    photographer = models.CharField(max_length=100, default='N. Minsi')

    def __str__(self):
        return f"Photo {self.number} taken on {self.date_taken}"


class Haiku(models.Model):
    number = models.AutoField(primary_key=True)
    text = models.TextField()
    author = models.CharField(max_length=100)
    instagram_tag = models.CharField(max_length=255, blank=True, null=True)  # New field for Instagram tag or URL
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)

    def get_instagram_link(self):
        if self.instagram_tag.startswith('http'):
            return self.instagram_tag  # If it's a full link
        return f"https://www.instagram.com/{self.instagram_tag.lstrip('@')}/"  # If it's a username
    
    def __str__(self):
        return self.text