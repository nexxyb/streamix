from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import View, FormView, TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# from .tokens import account_activation_token
from .models import User
from .forms import SignUpForm, LoginForm
from .tasks import send_verification_mail, welcome_email
# myapp/views.py


def login_view(request):
    # form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        print(email)
        print(password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
            
        else:
            msg = 'Incorrect email or password'

    return render(request, "users/login.html", { "msg": msg})

def verify_email_sent(request):
    return render(request, 'users/verify_email_sent.html')

def signup_success(request):
    return render(request, 'users/signup_success.html')

class SignupView(TemplateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('signup-success')
    # form_class= SignUpForm
    
    # def get(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     return self.render_to_response(self.get_context_data(form=form))
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.create_user(email=email,password=password)
        # user.set_password(password)
        # user.is_active = False
        user.is_active = True
        user.save()
        
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # token = default_token_generator.make_token(user)
        # activation_link = request.build_absolute_uri(reverse_lazy('activate', kwargs={'uidb64': uid, 'token': token}))
        
        # # send_verification_mail.delay(recipient=email,email=email, activation_link=activation_link)
        # send_verification_mail(recipient=email,email=email, activation_link=activation_link)
        
        return redirect(self.success_url)

class ActivateAccountView(View):
    success_url = reverse_lazy('home')
    
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            # user = authenticate(request, email=user.email)
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Add this line
            login(request, user)
            welcome_email.delay(user.email)
            return redirect(self.success_url)
        else:
            return HttpResponse('Activation link is invalid.')


def logout_view(request):
    
    logout(request)
    return redirect('index')

@login_required
def user_profile(request):
    user = request.user
    wallet= user.wallet
    context = {'user': user, 'wallet':wallet}
    return render(request, 'muse/profile.html', context)


    
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/custom_password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.email = request.POST.get('email')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
        