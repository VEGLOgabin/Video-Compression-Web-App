# videos/views.py
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Video
from .serializers import VideoSerializer
from .utils import compress_video
import os
from django.conf import settings
from rest_framework import status
from .models import Video
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import delete_video


class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        video_serializer = VideoSerializer(data=request.data)
        if video_serializer.is_valid():
            video = video_serializer.save()

            # Compress the video
            original_path = video.original_video.path
            compressed_path = os.path.join(settings.MEDIA_ROOT, 'videos/compressed', os.path.basename(original_path))
            if compress_video(original_path, compressed_path):
                video.compressed_video.name = os.path.relpath(compressed_path, settings.MEDIA_ROOT)
                video.save()

            # Schedule the deletion task to run after 1 hour
            delete_video.apply_async(args=[video.id], countdown=3600)

            return Response(video_serializer.data, status=201)
        return Response(video_serializer.errors, status=400)

class VideoDownloadView(APIView):
    def get(self, request, video_id, *args, **kwargs):
        try:
            video = Video.objects.get(id=video_id)
            if video.expired:
                return Response({"error": "This video has expired."}, status=status.HTTP_410_GONE)

            # Increment the download count
            video.download_count += 1
            video.save()

            # Return the compressed video file as a response
            response = FileResponse(video.compressed_video)
            response['Content-Disposition'] = f'attachment; filename="{video.original_name}"'
            return response
        except Video.DoesNotExist:
            return Response({"error": "Video not found."}, status=status.HTTP_404_NOT_FOUND)