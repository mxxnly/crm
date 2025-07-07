from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import Profile

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
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home') 
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

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