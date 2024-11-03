from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path
from .views import change_password  # Import the function-based view


urlpatterns = [
    path('', views.main, name='main'),
    path('haikus/', views.haikus_list, name='haikus'),  # Page to display all haikus
    path('haiku/create/', views.haiku_create, name='haiku_create'),  # Page to create a haiku
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('process_photos/', views.process_photos, name='process_photos'),
    path('process_csv/', views.process_csv, name='process_csv'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('login/', views.user_login, name='login'),  # Login page
    path('logout/', views.user_logout, name='logout'),  # Logout page
    path('change-password/', views.change_password, name='change_password'),
    path('search/', views.photo_search, name='photo_search'),  # Add this line
    path('random_photo/', views.random_photo, name='random_photo'),
    path('check-photo-errors/', views.check_photo_errors, name='check_photo_errors'),
]
# Serve media files in production if DEBUG is False
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)