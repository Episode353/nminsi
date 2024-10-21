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
    path('process_photos/', views.process_photos, name='process_photos'),
    path('process_csv/', views.process_csv, name='process_csv'),
    path('export_csv/', views.export_csv, name='export_csv'),
]
# Serve media files in production if DEBUG is False
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)