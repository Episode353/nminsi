from django.contrib import admin
from .models import Photo, Haiku

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('number', 'date_taken', 'collaborated', 'discard', 'done', 'wbord', 'insta', 'x', 'folder', 'gallery')
    list_filter = ('collaborated', 'discard', 'done', 'wbord', 'insta', 'x', 'folder', 'gallery')
    search_fields = ('number',)

class HaikuAdmin(admin.ModelAdmin):
    list_display = ('number', 'author', 'text', 'photo')
    list_filter = ('author', 'photo')
    search_fields = ('author', 'text')

# Register models with the custom admin classes
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Haiku, HaikuAdmin)
