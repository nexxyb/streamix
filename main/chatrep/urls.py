from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('devadmin/', admin.site.urls),
    path('',include('files.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/', include('allauth.urls')),
    path('account/', include('users.urls')),
    ]

# handler404 = 'repo.views.handler404'
# handler504 = 'repo.views.handler504'