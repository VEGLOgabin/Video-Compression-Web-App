# videos/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Video
import os
from django.conf import settings

@shared_task
def delete_video(video_id):
    video = Video.objects.get(id=video_id)
    if not video.expired:
        # Delete the original and compressed video files
        if video.original_video:
            os.remove(video.original_video.path)
        if video.compressed_video:
            os.remove(video.compressed_video.path)
        
        # Mark the video as expired
        video.expired = True
        video.save()