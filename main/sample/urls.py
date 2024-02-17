# myapp/urls.py
from django.urls import path
from .views import (
    category_view, channels_view, index_view, my_account_view,
    recommended_view, settings_view, single_channel_view,
    subscriptions_view, upload_edit_view, upload_video_view,
    video_detail_view, watch_history_view,
)

urlpatterns = [
    path('category/', category_view, name='category_view'),
    path('channels/', channels_view, name='channels_view'),
    path('index/', index_view, name='index_view'),
    path('my-account/', my_account_view, name='my_account_view'),
    path('recommended/', recommended_view, name='recommended_view'),
    path('settings/', settings_view, name='settings_view'),
    path('single-channel/', single_channel_view, name='single_channel_view'),
    path('subscriptions/', subscriptions_view, name='subscriptions_view'),
    path('upload-edit/', upload_edit_view, name='upload_edit_view'),
    path('upload-video/', upload_video_view, name='upload_video_view'),
    path('video-detail/', video_detail_view, name='video_detail_view'),
    path('watch-history/', watch_history_view, name='watch_history_view'),
]
