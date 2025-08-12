import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamilnadu_tourism.settings')
django.setup()

from destinations.models import TouristPlace
from django.db.models import Count

# 1. Remove places with names containing '(Branch'
branch_places = TouristPlace.objects.filter(name__icontains='(Branch')
count_branch = branch_places.count()
branch_places.delete()
print(f"Deleted {count_branch} 'Branch' duplicate places.")

# 2. Remove exact duplicates by name (keep the first, delete the rest)
duplicates = (
    TouristPlace.objects.values('name')
    .annotate(name_count=Count('name'))
    .filter(name_count__gt=1)
)

total_deleted = 0
for dup in duplicates:
    places = list(TouristPlace.objects.filter(name=dup['name']).order_by('id'))
    for place in places[1:]:
        place.delete()
        total_deleted += 1

print(f"Deleted {total_deleted} exact duplicate places by name.")

# 3. Remove places with repeated images (keep only one per image)
image_duplicates = (
    TouristPlace.objects.values('image')
    .annotate(image_count=Count('image'))
    .filter(image_count__gt=1)
)

image_deleted = 0
for dup in image_duplicates:
    places = list(TouristPlace.objects.filter(image=dup['image']).order_by('id'))
    for place in places[1:]:
        place.delete()
        image_deleted += 1

print(f"Deleted {image_deleted} places with repeated images (kept one per image).")
print("Full duplicate cleanup complete.") 