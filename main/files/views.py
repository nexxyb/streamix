# files/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import subprocess
from .models import Video
from .tasks import process_video
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



def category_view(request):
    return render(request, 'files/category.html')

def channels_view(request):
    return render(request, 'files/channels.html')

def index_view(request):
    return render(request, 'files/index.html')

def my_account_view(request):
    return render(request, 'files/my_account.html')

def recommended_view(request):
    return render(request, 'files/recommended.html')

def settings_view(request):
    return render(request, 'files/settings.html')

def single_channel_view(request):
    return render(request, 'files/single_channel.html')

def subscriptions_view(request):
    return render(request, 'files/subscriptions.html')

# def upload_edit_view(request):
#     return render(request, 'files/upload_edit.html')

def upload_edit_view(request,pk):
    video=Video.objects.get(id=pk)
    
    return render(request, 'files/upload_edit.html', {'video':video})

@csrf_exempt
@login_required
def upload_video_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        files = request.FILES.getlist('file')
        if files:
            for video_file in files:
                video = Video.objects.create(user=request.user, title=video_file.name,video_file=video_file)
                process_video.delay(video.id)

                # return redirect('upload_edit_view', pk=video.pk)
                JsonResponse({'id': video.id,})
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    return render(request, 'files/upload_video.html')

def video_detail_view(request):
    return render(request, 'files/video_detail.html')

def watch_history_view(request):
    return render(request, 'files/watch_history.html')
