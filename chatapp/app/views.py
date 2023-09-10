from .models import UserProfile, Chat
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('lists')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def chat(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Retrieve chats for the logged-in user
    user_profile = UserProfile.objects.get(user=request.user)
    chats = Chat.objects.filter(participants=user_profile)

    context = {'chats': chats}
    return render(request, 'chat.html', context)
