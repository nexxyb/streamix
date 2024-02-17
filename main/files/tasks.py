
from celery import shared_task
from .models import Video, EncodedVideo, Subtitle
from moviepy.editor import VideoFileClip
from .utils import convert_and_save,generate_srt_subtitles,generate_video_thumbnail
import os

@shared_task
def process_video(video_id):
    try:
        video = Video.objects.get(pk=video_id)
        
        encode_video.delay(video.id)
        extract_subtitle.delay(video.id)
        # extract_metadata.delay(video.id)
        generate_thumbnail.delay(video.id)
    except Video.DoesNotExist:
        print(f"Video with id {video_id} does not exist.")
    except Exception as e:
        print(f"Error processing video {video_id}: {e}")


@shared_task
def encode_video(video_id):
    
    video_instance = Video.objects.get(pk=video_id)
    path = video_instance.video_file.path

    video_clip = VideoFileClip(path)
    duration = video_clip.duration
    video_instance.durution = duration
    video_instance.save()
    
    target_resolutions = ["240p", "360p", "480p", "720p", "1080p"]

    for resolution in target_resolutions:
        encoded = convert_and_save(path, resolution)
        
        encoded_video = EncodedVideo.objects.create(
            video=video_instance, 
            file=encoded,
            resolution=resolution,
            bitrate=int(os.path.getsize(encoded) * 8 / duration)
        )

        encoded_video.save()


@shared_task
def extract_subtitle(video_id):
    try:
        video = Video.objects.get(pk=video_id)
        text,language = generate_srt_subtitles(video.video_file.path)
        
        Subtitle.objects.create(video=video, language=language, text=text)

        
    except Video.DoesNotExist:
        print(f"Video with id {video_id} does not exist.")
    except Exception as e:
        print(f"Error extracting subtitle for video {video_id}: {e}")


@shared_task
def generate_thumbnail(id):
    try:
        video = Video.objects.get(pk=id)
        video_clip = video.video_file.path
        thumbnail_size = (320, 180)

        thumbnail = generate_video_thumbnail(video_clip, 5, thumbnail_size)

        # Save the thumbnail image
        thumbnail.save(f"{video.video_file.name}_thumbnail.jpg")
        video.thumbnail = f"{video.video_file.name}_thumbnail.jpg"
        video.save()
    except Video.DoesNotExist:
        print(f"Video with id {id} does not exist.")
    except Exception as e:
        print(f"Error generating thumbnail for video {id}: {e}")