from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Photo, Haiku

def main(request):
    # Fetch all photos from the database
    photo_list = Photo.objects.all()
    
    # Set up pagination
    paginator = Paginator(photo_list, 12)  # Display 12 photos per page
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)

    return render(request, 'index.html', {'photos': photos})

def fonts(request):
    return render(request, 'fonts.html')

def haiku_create(request):
    if request.method == "POST":
        text = request.POST.get('text')
        author = request.POST.get('author')
        haiku = Haiku(text=text, author=author)
        haiku.save()
        return redirect('main')  # Redirect to the main page after saving
    return render(request, 'haiku_create.html')  # Create a template for this view

def photo_detail(request, photo_id):
    # Fetch the photo based on the provided ID
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'photo_detail.html', {'photo': photo})  # Create a template for the photo detail view
