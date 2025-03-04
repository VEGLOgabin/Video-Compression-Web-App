# videos/models.py
from django.db import models
from django.utils import timezone

class Video(models.Model):
    # Original video file
    original_video = models.FileField(upload_to='videos/original/')
    
    # Compressed video file
    compressed_video = models.FileField(upload_to='videos/compressed/', null=True, blank=True)
    
    # Metadata
    original_name = models.CharField(max_length=255, blank=True)  # Original file name
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Upload timestamp
    download_count = models.PositiveIntegerField(default=0)  # Track download count
    expired = models.BooleanField(default=False)  # Flag to indicate if the video has expired

    def __str__(self):
        return self.original_name