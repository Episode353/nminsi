import os
import csv
import re
from datetime import date

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .models import Photo, Haiku

def main(request):
    # Fetch all photos from the database
    photo_list = Photo.objects.all()

    # Handle sorting
    sort_option = request.GET.get('sort', 'number_asc')  # Default to 'number ascending'
    
    if sort_option == 'date':
        photo_list = photo_list.order_by('date_taken')
    elif sort_option == 'collaborated':
        photo_list = photo_list.filter(collaborated=True).order_by('number')
    elif sort_option == 'not_collaborated':
        photo_list = photo_list.filter(collaborated=False).order_by('number')
    elif sort_option == 'collaborated_not_posted':
        # Assuming you have a field 'posted' to indicate if a photo has been posted
        photo_list = photo_list.filter(collaborated=True, posted=False).order_by('number')
    elif sort_option == 'number_desc':
        photo_list = photo_list.order_by('-number')  # Sort by number descending
    elif sort_option == 'insta_asc':
        photo_list = photo_list.order_by('insta')  # Sort by Instagram ascending
    elif sort_option == 'insta_desc':
        photo_list = photo_list.order_by('-insta')  # Sort by Instagram descending
    else:
        photo_list = photo_list.order_by('number')  # Sort by number ascending

    # Set up pagination
    paginator = Paginator(photo_list, 45)  # Display 45 photos per page
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)

    return render(request, 'index.html', {'photos': photos, 'request': request})




def haikus_list(request):
    sort_option = request.GET.get('sort', 'all')  # Default to 'all'

    if sort_option == 'with_photo':
        haikus = Haiku.objects.filter(photo__isnull=False)
    elif sort_option == 'without_photo':
        haikus = Haiku.objects.filter(photo__isnull=True)
    else:
        haikus = Haiku.objects.all()

    paginator = Paginator(haikus, 20)  # Display 20 haikus per page
    page_number = request.GET.get('page')
    haikus_page = paginator.get_page(page_number)

    return render(request, 'haikus_list.html', {'haikus': haikus_page, 'sort_option': sort_option})

from .models import Haiku, Photo, Profile
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Haiku, Photo, Profile

@login_required
def haiku_create(request):
    # Handle POST request for haiku creation
    if request.method == "POST":
        # Get the user's profile, or create it if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=request.user)

        # Extract haiku text from POST data
        text = request.POST.get('text')
        
        # Get the photo number from the form or URL
        photo_number = request.POST.get('photo_number') or request.GET.get('photo_number')

        # Get author name from the user's profile or use the username
        author_name = profile.author_name if profile.author_name else request.user.username
        instagram_tag = profile.instagram_handle

        # Create a Haiku object with the provided data
        haiku = Haiku(text=text, author=author_name, instagram_tag=instagram_tag)

        # Associate the Haiku with a photo if a valid photo_number is provided
        photo = None  # Initialize photo here
        if photo_number:
            try:
                photo = Photo.objects.get(number=photo_number)
                haiku.photo = photo
            except Photo.DoesNotExist:
                return HttpResponse(f"Photo with number {photo_number} does not exist.")

        # Save the Haiku
        haiku.save()

        # Redirect to the haikus list page
        # Check if photo is not None before accessing its id
        if photo is not None:
            return redirect('photo_detail', photo_id=photo.id)
        else:
            # Redirect to a different page if there's no photo associated
            return redirect('haikus')  # Or any other appropriate page

    # Handle GET request to pre-fill the form with the selected photo
    photo_number = request.GET.get('photo_number')
    photo = None
    if photo_number:
        photo = get_object_or_404(Photo, number=photo_number)

    return render(request, 'haiku_create.html', {'photo': photo})




def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    haikus = Haiku.objects.filter(photo=photo)  # Get haikus associated with the photo
    return render(request, 'photo_detail.html', {'photo': photo, 'haikus': haikus})

@login_required
def process_photos(request):
    media_folder = os.path.join(settings.MEDIA_ROOT, 'photos')
    updates = []

    existing_photos = Photo.objects.all().values_list('photo', flat=True)
    existing_photo_files = set([os.path.basename(photo_path) for photo_path in existing_photos])
    insta_pattern = re.compile(r"InstaPics-(\d+)-\d{4}-\d{2}-\d{2}\.jpg")

    if os.path.exists(media_folder):
        for filename in os.listdir(media_folder):
            if filename == '.DS_Store':
                continue

            if filename not in existing_photo_files:
                insta_match = insta_pattern.match(filename)

                if insta_match:
                    photo_id = int(insta_match.group(1))

                    try:
                        existing_photo = Photo.objects.get(number=photo_id)
                        updates.append(f'Found existing photo with ID: {photo_id}.')
                        existing_photo.photo = f'photos/{filename}'
                        existing_photo.date_taken = date.today()
                        existing_photo.save()
                        continue

                    except Photo.DoesNotExist:
                        updates.append(f'InstaPics pattern found, ID: {photo_id}. Creating new.')
                        new_photo = Photo.objects.create(
                            date_taken=date.today(),
                            photo=f'photos/{filename}',
                            number=photo_id
                        )
                        updates.append(f'Added {filename} as photo {new_photo.number}.')

                else:
                    match = re.search(r"\d+", filename)
                    photo_number = int(match.group(0)) if match else Photo.objects.count() + 1

                    new_photo = Photo.objects.create(
                        date_taken=date.today(),
                        photo=f'photos/{filename}',
                        number=photo_number
                    )
                    updates.append(f'Added {filename} as photo {new_photo.number}.')
            else:
                updates.append(f'{filename} already exists in the database.')

    else:
        updates.append("Media folder does not exist.")

    return HttpResponse('<br>'.join(updates))

import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import Photo, Haiku

@login_required
def process_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.endswith('.csv'):
            return HttpResponse('This is not a CSV file.')

        file_data = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(file_data)
        updates = []

        for row in reader:
            file_name = row.get('File Name', '').strip()
            photo_number = None

            if file_name.startswith("Instapics-"):
                parts = file_name.split('-')
                if len(parts) >= 3:
                    photo_number = int(parts[1])
            elif row.get('#', '').strip().isdigit():
                photo_number = int(row['#'].strip())

            if photo_number is not None:
                photo = Photo.objects.filter(number=photo_number).first()
                if photo is None:
                    updates.append(f"Photo number {photo_number} does not exist.")
                    continue

                # Update existing fields
                photo.discard = row.get('Discard', '').upper() == 'TRUE'
                photo.done = row.get('Done', '').upper() == 'TRUE'
                photo.wbord = row.get('Wbord', '').upper() == 'TRUE'
                photo.insta = row.get('Insta', '').upper() == 'TRUE'
                photo.x = row.get('X', '').upper() == 'TRUE'
                photo.folder = row.get('Folder', '').upper() == 'TRUE'
                photo.gallery = row.get('Gallery', '').upper() == 'TRUE'
                photo.collaborated = photo.done
                photo.photographer = row.get('Photographer', '').strip() or 'Unknown'

                # Update new fields with defaults if missing
                photo.queued = row.get('Queued', 'FALSE').upper() == 'TRUE'
                photo.posted = row.get('Posted', 'FALSE').upper() == 'TRUE'
                photo.authentication = row.get('Authentication', '').strip()

                # Handle Haiku details if provided
                haiku_text = row.get('Haiku', '').strip()
                author = row.get('Author', '').strip() or 'N. Minsi'
                instagram_tag = row.get('Instagram Tag', '').strip()

                if haiku_text:
                    # Using filter to avoid MultipleObjectsReturned
                    haiku_queryset = Haiku.objects.filter(photo=photo)
                    
                    if haiku_queryset.exists():
                        # If there are multiple haikus, just select the first one
                        haiku = haiku_queryset.first()
                        haiku.text = haiku_text
                        haiku.author = author
                        haiku.instagram_tag = instagram_tag
                        haiku.save()
                    else:
                        # If no haiku exists, create a new one
                        haiku = Haiku.objects.create(photo=photo, text=haiku_text, author=author, instagram_tag=instagram_tag)


              # Update date_posted from the CSV row
                date_posted_str = row.get('Date Posted', '').strip()
                if date_posted_str:
                    try:
                        # Try to parse as YYYY-MM-DD first
                        photo.date_posted = date.fromisoformat(date_posted_str)
                    except ValueError:
                        # If it fails, try to parse as MM/DD/YYYY
                        try:
                            month, day, year = map(int, date_posted_str.split('/'))
                            photo.date_posted = date(year, month, day)
                        except ValueError:
                            updates.append(f"Invalid date format for photo number {photo_number}: {date_posted_str}")


                photo.save()
                updates.append(f"Updated photo number {photo_number} successfully.")

        return render(request, 'process_csv.html', {'updates': updates})

    return render(request, 'process_csv.html')




@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="photos_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['#', 'File Name', 'Discard', 'Done', 'Wbord', 'Insta', 'X', 'Folder', 'Gallery', 'Haiku', 'Author', 'Photographer', 'Instagram Tag', 'Queued', 'Posted', 'Authentication', 'Date Posted'])  # Add Date Posted header

    photos = Photo.objects.all()

    for photo in photos:
        haiku = Haiku.objects.filter(photo=photo).first()
        haiku_text = haiku.text if haiku else ''
        haiku_author = haiku.author if haiku else ''
        instagram_tag = haiku.instagram_tag if haiku else ''
        
        writer.writerow([
            photo.number,
            photo.photo.name,
            'TRUE' if photo.discard else 'FALSE',
            'TRUE' if photo.done else 'FALSE',
            'TRUE' if photo.wbord else 'FALSE',
            'TRUE' if photo.insta else 'FALSE',
            'TRUE' if photo.x else 'FALSE',
            'TRUE' if photo.folder else 'FALSE',
            'TRUE' if photo.gallery else 'FALSE',
            haiku_text,
            haiku_author,
            photo.photographer,
            instagram_tag,
            'TRUE' if photo.queued else 'FALSE',  # Export queued status
            'TRUE' if photo.posted else 'FALSE',  # Export posted status
            photo.authentication or '',  # Export authentication text
            photo.date_posted.strftime('%Y-%m-%d') if photo.date_posted else '',  # Export Date Posted
        ])

    return response





def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('main')  # Redirect to the main page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('main')  # Redirect to the login page

# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')  # Redirect to the same page or any other page you prefer
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

from django.db.models import Q

def photo_search(request):
    query = request.GET.get('q', '')
    # Filter photos based on the search query
    photos = Photo.objects.filter(
            Q(number__icontains=query) |
            Q(photographer__icontains=query) |
            Q(haiku__text__icontains=query) |
            Q(haiku__author__icontains=query)
        ).distinct()  # Use distinct() to avoid duplicate photos

    # Set up pagination
    paginator = Paginator(photos, 45)  # Display 45 photos per page
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)

    return render(request, 'search_results.html', {'photos': photos, 'query': query})

import random
from django.shortcuts import redirect

def random_photo(request):
    photo_count = Photo.objects.count()
    if photo_count > 0:
        random_index = random.randint(0, photo_count - 1)
        random_photo = Photo.objects.all()[random_index]
        return redirect('photo_detail', photo_id=random_photo.id)
    else:
        return redirect('main')  # If no photos exist, redirect to the main page

from django.shortcuts import render
from .models import Photo

@login_required
def check_photo_errors(request):
    # Query photos with error 1: posted_date has a date but posted is False
    error_1_photos = Photo.objects.filter(date_posted__isnull=False, posted=False)

    # Query photos with error 2: posted is True, but posted_date is empty
    error_2_photos = Photo.objects.filter(posted=True, date_posted__isnull=True)

    # Render these photos in the template
    return render(request, 'check_photo_errors.html', {
        'error_1_photos': error_1_photos,
        'error_2_photos': error_2_photos,
    })
