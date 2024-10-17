from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('haikus/', views.haikus_list, name='haikus'),  # Page to display all haikus
    path('haiku/create/', views.haiku_create, name='haiku_create'),  # Page to create a haiku
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('admin/', admin.site.urls),
    path('fonts/', views.fonts, name='fonts'),
    path('process_photos/', views.process_photos, name='process_photos'),
    path('process_csv/', views.process_csv, name='process_csv'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Add this line for serving media files
