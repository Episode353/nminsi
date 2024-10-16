from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Photo, Haiku

def main(request):
    # Fetch all photos from the database
    photo_list = Photo.objects.all()
    
    # Set up pagination
    paginator = Paginator(photo_list, 12)
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)

    return render(request, 'index.html', {'photos': photos})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo, Haiku

from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo, Haiku

def haiku_create(request):
    if request.method == "POST":
        text = request.POST.get('text')
        author = request.POST.get('author')
        photo_id = request.POST.get('photo_id')  # Get photo ID from POST data
        
        # Create Haiku without a photo if photo_id is not provided
        haiku = Haiku(text=text, author=author)
        if photo_id:
            haiku.photo_id = photo_id  # Only associate if photo_id is present
        haiku.save()
        return redirect('haikus')  # Redirect to the haikus page after saving

    # If GET, retrieve the photo_id from query parameters
    photo_id = request.GET.get('photo_id')
    photo = None
    if photo_id:
        photo = get_object_or_404(Photo, id=photo_id)  # Ensure the photo exists

    return render(request, 'haiku_create.html', {'photo': photo})  # Pass the photo to the template (if exists)


def haikus_list(request):
    haikus = Haiku.objects.all()
    paginator = Paginator(haikus, 10)  # Display 10 haikus per page
    page_number = request.GET.get('page')
    haikus_page = paginator.get_page(page_number)
    return render(request, 'haikus_list.html', {'haikus': haikus_page})

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_detail.html', {'photo': photo})  # Render photo detail page

def fonts(request):
    return render(request, 'fonts.html')
