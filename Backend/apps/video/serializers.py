# videos/serializers.py
from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    # original_video = serializers.FileField()  # Explicitly define it

    class Meta:
        model = Video
        fields = ['id', 'original_video', 'original_name', 'uploaded_at', 'download_count', 'expired']