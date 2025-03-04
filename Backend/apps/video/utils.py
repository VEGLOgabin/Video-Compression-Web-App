# videos/utils.py
import os
import ffmpeg
from django.conf import settings

def compress_video(input_path, output_path):
    try:
        # Compress the video using FFmpeg
        ffmpeg.input(input_path).output(output_path, vcodec='libx265', crf=28).run()
        return True
    except Exception as e:
        print(f"Error compressing video: {e}")
        return False