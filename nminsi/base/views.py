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

import os
import csv  # Add this line
from django.conf import settings
from django.http import HttpResponse
from .models import Photo
from datetime import date
import re


from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo, Haiku

def haiku_create(request):
    if request.method == "POST":
        text = request.POST.get('text')
        author = request.POST.get('author')
        photo_number = request.POST.get('photo_number')  # Use 'photo_number' instead of 'photo_id'
        
        # Create Haiku without a photo if photo_number is not provided
        haiku = Haiku(text=text, author=author)
        if photo_number:
            try:
                # Use the number field to get the Photo instance
                photo = Photo.objects.get(number=photo_number)
                haiku.photo = photo  # Associate the haiku with the photo
            except Photo.DoesNotExist:
                # Handle the case where the photo does not exist
                return HttpResponse(f"Photo with number {photo_number} does not exist.")
        
        haiku.save()
        return redirect('haikus')  # Redirect to the haikus page after saving

    # If GET, retrieve the photo_number from query parameters
    photo_number = request.GET.get('photo_number')
    photo = None
    if photo_number:
        photo = get_object_or_404(Photo, number=photo_number)  # Ensure the photo exists

    return render(request, 'haiku_create.html', {'photo': photo})  # Pass the photo to the template (if exists)




def haikus_list(request):
    haikus = Haiku.objects.all()
    paginator = Paginator(haikus, 10)  # Display 10 haikus per page
    page_number = request.GET.get('page')
    haikus_page = paginator.get_page(page_number)
    return render(request, 'haikus_list.html', {'haikus': haikus_page})

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    haikus = Haiku.objects.filter(photo=photo)  # Get haikus associated with the photo
    return render(request, 'photo_detail.html', {'photo': photo, 'haikus': haikus})  # Pass haikus to the template


def fonts(request):
    return render(request, 'fonts.html')

import os
from django.conf import settings
from django.http import HttpResponse
from .models import Photo
from datetime import date
import re

def process_photos(request):
    # Path to the folder containing photos
    media_folder = os.path.join(settings.MEDIA_ROOT, 'photos')

    # Initialize an empty list to store update messages
    updates = []

    # Get all existing Photo objects
    existing_photos = Photo.objects.all().values_list('photo', flat=True)
    existing_photo_files = set([os.path.basename(photo_path) for photo_path in existing_photos])

    # Regex pattern for matching "InstaPics-{id}-(date).jpg"
    insta_pattern = re.compile(r"InstaPics-(\d+)-\(\d+\)\.jpg")

    # List all files in the 'photos' folder
    if os.path.exists(media_folder):
        for filename in os.listdir(media_folder):
            # Check if the file is already in the Photo model
            if filename not in existing_photo_files:
                # Determine if the filename matches the InstaPics pattern
                insta_match = insta_pattern.match(filename)

                if insta_match:
                    # Extract the ID from the regex match
                    photo_id = int(insta_match.group(1))  # Ensure ID is an integer

                    try:
                        # Attempt to find a Photo with the extracted ID
                        existing_photo = Photo.objects.get(id=photo_id)
                        updates.append(f'Found existing photo with ID: {photo_id}.')

                        # Update existing photo with filename and date
                        existing_photo.photo = f'photos/{filename}'
                        existing_photo.date_taken = date.today()
                        existing_photo.save()
                        continue  # Skip creating a new photo since it exists

                    except Photo.DoesNotExist:
                        # If photo with ID doesn't exist, create a new one
                        updates.append(f'InstaPics pattern found, ID: {photo_id}. Photo not found. Creating new.')
                        new_photo = Photo.objects.create(
                            date_taken=date.today(),
                            photo=f'photos/{filename}',
                            number=photo_id  # Use extracted ID as number
                        )
                        updates.append(f'Added {filename} as photo {new_photo.number}.')

                else:
                    # Handle other filenames directly
                    new_photo = Photo.objects.create(
                        date_taken=date.today(),
                        photo=f'photos/{filename}',
                        number=Photo.objects.count() + 1  # Use count for non-InstaPics photos
                    )
                    updates.append(f'Added {filename} as photo {new_photo.number}.')

            else:
                updates.append(f'{filename} already exists in the database.')

    else:
        updates.append("Media folder does not exist.")

    # Return updates as a simple HTTP response
    return HttpResponse('<br>'.join(updates))

def process_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('This is not a CSV file.')

        file_data = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(file_data)
        updates = []

        for row in reader:
            file_name = row['File Name'].strip()
            photo_number = None
            
            if file_name.startswith("Instapics-"):
                parts = file_name.split('-')
                if len(parts) >= 3:
                    photo_number = int(parts[1])  # Extract ID as integer from filename
            elif row['#'].strip().isdigit():
                photo_number = int(row['#'].strip())  # Use row number if applicable

            if photo_number is not None:
                try:
                    # Fetch the Photo by its number
                    photo = Photo.objects.get(number=photo_number)

                    # Update photo attributes
                    photo.discard = row['Discard'].upper() == 'TRUE'
                    photo.done = row['Done'].upper() == 'TRUE'
                    photo.wbord = row['Wbord'].upper() == 'TRUE'
                    photo.insta = row['Insta'].upper() == 'TRUE'
                    photo.x = row['X'].upper() == 'TRUE'
                    photo.folder = row['Folder'].upper() == 'TRUE'
                    photo.gallery = row['Gallery'].upper() == 'TRUE'

                    # Set 'collaborated' to True if 'done' is True
                    if photo.done:
                        photo.collaborated = True
                    else:
                        photo.collaborated = False  # Optional: reset 'collaborated' if 'done' is False

                    # Update or create haiku
                    haiku_text = row['Haiku'].strip()
                    if haiku_text:
                        haiku, created = Haiku.objects.update_or_create(
                            photo=photo,
                            defaults={'text': haiku_text, 'author': row['Author'].strip()}
                        )

                    photo.save()
                    updates.append(f"Updated photo number {photo_number} successfully.")

                except Photo.DoesNotExist:
                    updates.append(f"Photo number {photo_number} does not exist.")
                except Photo.MultipleObjectsReturned:
                    updates.append(f"Multiple photos found for number {photo_number}.")

        return render(request, 'process_csv.html', {'updates': updates})
    return render(request, 'process_csv.html')

import csv
from django.http import HttpResponse
from .models import Photo, Haiku

def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="photos_export.csv"'

    writer = csv.writer(response)

    # Write CSV headers (adjust this to match your import format)
    writer.writerow(['#', 'File Name', 'Discard', 'Done', 'Wbord', 'Insta', 'X', 'Folder', 'Gallery', 'Haiku', 'Author'])

    # Query the database for all Photo records
    photos = Photo.objects.all()

    for photo in photos:
        # Get associated haiku if it exists
        haiku = Haiku.objects.filter(photo=photo).first()
        haiku_text = haiku.text if haiku else ''
        haiku_author = haiku.author if haiku else ''

        # Write each photo's data into a row (match the import format)
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
            haiku_author
        ])

    return response
