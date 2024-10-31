from django.contrib import admin
from .models import Photo, Haiku, Profile

class PhotoAdmin(admin.ModelAdmin):
    # List display to show all fields of the Photo model
    list_display = (
        'number', 'date_taken', 'collaborated', 'discard', 'done', 
        'wbord', 'insta', 'x', 'folder', 'gallery', 
        'photographer', 'queued', 'posted', 'authentication'
    )
    
    # Filters to narrow down the list by certain fields
    list_filter = (
        'collaborated', 'discard', 'done', 'wbord', 
        'insta', 'x', 'folder', 'gallery', 'queued', 'posted'
    )
    
    # Fields to search within the Photo model
    search_fields = ('number', 'photographer', 'authentication')

class HaikuAdmin(admin.ModelAdmin):
    list_display = ('number', 'author', 'text', 'photo')
    list_filter = ('author', 'photo')
    search_fields = ('author', 'text')

# Register models with the custom admin classes
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Haiku, HaikuAdmin)
admin.site.register(Profile)
