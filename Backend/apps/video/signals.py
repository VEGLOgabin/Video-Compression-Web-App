# video/signals.py
import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Video

@receiver(post_delete, sender=Video)
def delete_video_files(sender, instance, **kwargs):
    """Delete video files when a Video object is deleted."""
    if instance.original_video:
        if os.path.exists(instance.original_video.path):
            os.remove(instance.original_video.path)
    if instance.compressed_video:
        if os.path.exists(instance.compressed_video.path):
            os.remove(instance.compressed_video.path)

@receiver(pre_save, sender=Video)
def cleanup_old_file(sender, instance, **kwargs):
    """Delete old video files when a new file is uploaded (overwrite case)."""
    if not instance.pk:
        return  # Only run for existing objects

    try:
        old_instance = Video.objects.get(pk=instance.pk)
        if old_instance.original_video and old_instance.original_video != instance.original_video:
            if os.path.exists(old_instance.original_video.path):
                os.remove(old_instance.original_video.path)

        if old_instance.compressed_video and old_instance.compressed_video != instance.compressed_video:
            if os.path.exists(old_instance.compressed_video.path):
                os.remove(old_instance.compressed_video.path)
    except Video.DoesNotExist:
        pass
