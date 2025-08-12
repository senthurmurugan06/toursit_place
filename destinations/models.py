from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class TouristPlace(models.Model):
    CATEGORY_CHOICES = [
        ('Temple', 'Temple'),
        ('Beach', 'Beach'),
        ('Hill Station', 'Hill Station'),
        ('Monument', 'Monument'),
        ('Wildlife', 'Wildlife'),
        ('Waterfall', 'Waterfall'),
        ('Fort', 'Fort'),
        ('Garden', 'Garden'),
        ('Museum', 'Museum'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='places/')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    district = models.CharField(max_length=50)
    short_description = models.TextField(max_length=300)
    detailed_description = models.TextField(blank=True, null=True)
    how_to_reach = models.TextField(blank=True, null=True)
    best_time_to_visit = models.CharField(max_length=100, blank=True, null=True)
    entry_fee = models.CharField(max_length=100, blank=True, null=True)
    timings = models.CharField(max_length=100, blank=True, null=True)
    nearby_attractions = models.TextField(blank=True, null=True)
    accommodation = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    featured = models.BooleanField(default=False)  # For carousel
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'place']

    def __str__(self):
        return f"{self.user.username} - {self.place.name}"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Chat: {self.message[:50]}..."
