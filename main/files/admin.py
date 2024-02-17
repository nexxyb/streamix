
from django.contrib import admin
from .models import Video, EncodedVideo, Subtitle

admin.site.register(Video)
admin.site.register(EncodedVideo)
admin.site.register(Subtitle)
