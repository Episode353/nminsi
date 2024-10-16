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

def haiku_create(request):
    if request.method == "POST":
        text = request.POST.get('text')
        author = request.POST.get('author')
        photo_id = request.POST.get('photo_id')  # Get photo ID if submitted from photo detail
        haiku = Haiku(text=text, author=author, photo_id=photo_id)
        haiku.save()
        return redirect('haikus')  # Redirect to the haikus page after saving
    return render(request, 'haiku_create.html')  # Render haiku creation form

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
