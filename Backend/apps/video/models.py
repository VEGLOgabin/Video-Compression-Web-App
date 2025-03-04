# videos/models.py
from django.db import models
from django.utils import timezone
import os
import ffmpeg
from django.conf import settings
import threading
import time

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
    
    def compress_video(self):
        """Compress the video and save the path in compressed_video field."""
        if not self.original_video:
            return False

        original_path = self.original_video.path
        compressed_path = os.path.join(settings.MEDIA_ROOT, 'videos/compressed', os.path.basename(original_path))

        try:
            ffmpeg.input(original_path).output(compressed_path, vcodec='libx265', crf=28).run()
            self.compressed_video.name = os.path.relpath(compressed_path, settings.MEDIA_ROOT)
            self.save()
            return True
        except Exception as e:
            print(f"Error compressing video: {e}")
            return False

    def delete_video(self):
        """Delete the video files and mark as expired."""
        if self.expired:
            return
        
        if self.original_video:
            os.remove(self.original_video.path)
        if self.compressed_video:
            os.remove(self.compressed_video.path)

        self.expired = True
        self.save()

    def schedule_deletion(self, delay=3600):
        """Schedule video deletion after a certain delay (default: 1 hour)."""
        def delayed_delete(video_id, delay):
            time.sleep(delay)
            try:
                video = Video.objects.get(id=video_id)
                video.delete_video()
            except Video.DoesNotExist:
                pass

        thread = threading.Thread(target=delayed_delete, args=(self.id, delay))
        thread.start()
    
    class Meta:
        ordering = ("-uploaded_at",)
        db_table = 'Video'