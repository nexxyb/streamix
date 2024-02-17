# files/views.py
from django.shortcuts import render

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

def upload_edit_view(request):
    return render(request, 'files/upload_edit.html')

def upload_video_view(request):
    return render(request, 'files/upload_video.html')

def video_detail_view(request):
    return render(request, 'files/video_detail.html')

def watch_history_view(request):
    return render(request, 'files/watch_history.html')
