from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, EmailCodeForm
from .models import Profile
from django.core.mail import send_mail
from .models import CustomUser


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Невірний логін або пароль')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# views.

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            code = user.generate_confirmation_code()

            send_mail(
                'Your confirmation code',
                f'Your verification code is: {code}',
                'noreply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )

            request.session['pending_user_id'] = user.id
            return redirect('verify_email')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# views.py
def verify_email_view(request):
    if request.method == 'POST':
        form = EmailCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user_id = request.session.get('pending_user_id')
            user = CustomUser.objects.filter(id=user_id, email_confirmation_code=code).first()
            if user:
                user.is_active = True
                user.email_confirmation_code = None
                user.save()
                messages.success(request, "Your email has been confirmed. You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Invalid code.")
    else:
        form = EmailCodeForm()
    return render(request, 'verify_email.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')

def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    context = {
        'profile':profile,
    }
    return render(request, "profile.html", context)