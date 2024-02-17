from django.urls import path, include
from . import views
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views


urlpatterns = [
    #users
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('email_verification_sent/', views.verify_email_sent, name='verify_email_sent'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup-success/', views.signup_success, name='signup-success'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    # path('send-all/', views.SendAll.as_view(), name='send-all'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done1.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]

