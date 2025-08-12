from django.contrib import admin
from .models import TouristPlace, Favorite

@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'category', 'featured', 'created_at']
    list_filter = ['category', 'district', 'featured']
    search_fields = ['name', 'district', 'short_description']

admin.site.register(Favorite)
