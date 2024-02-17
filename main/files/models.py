from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.contrib.auth import get_user_model

User=get_user_model()
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    views = models.IntegerField(default=0)
    duration = models.IntegerField(blank=True, null=True)
    orientation = models.CharField(max_length=20, default="")
    privacy= models.CharField(max_length=10, default="public")
    language= models.CharField(max_length=10, default="english")
    monetize= models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    
    

    def __str__(self):
        return self.title

class EncodedVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    file = models.FileField(upload_to='encoded_videos/')
    resolution = models.CharField(max_length=10)
    bitrate = models.IntegerField()

    def __str__(self):
        return self.file.name

class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='subtitles')
    language = models.CharField(max_length=2)  
    text =  models.TextField()

class Tag(models.Model):
    """A Tag model"""
    tag = models.CharField(max_length=100, unique=True, db_index=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='tags')
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag