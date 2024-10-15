from django.contrib import admin
from .models import Photo, Haiku


# Register models with the admin site
admin.site.register(Photo)
admin.site.register(Haiku)
