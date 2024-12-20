from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm
from .models import Playlist,UserProfile
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return render(request, 'music/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'music/login.html')


from django.contrib.auth.hashers import make_password

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        age = request.POST.get('age')  # Get age from the form
        bio = request.POST.get('bio')  # Get bio from the form
        profile_picture = request.FILES.get('profile_picture')  # Handle profile picture

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'music/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return render(request, 'music/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'music/register.html')

        # Save the user
        user = User(username=username, email=email)
        user.password = make_password(password)  # Hash the password
        user.save()

        # Create the user profile
        UserProfile.objects.create(
            user=user,
            age=age if age else None,
            bio=bio,
            profile_picture=profile_picture
        )

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'music/register.html')


def main_view(request):
    return render(request, 'music/main.html')

@login_required
def personality_quiz_view(request):
    return render(request, 'music/personality_quiz.html')

@login_required
def profile_view(request):
    return render(request, 'music/profile.html')

@login_required
def generate_playlist_view(request):
    # This would integrate with Spotify API to generate playlists
    mood = request.GET.get('mood', '')
    activity = request.GET.get('activity', '')
    
    playlists = Playlist.objects.filter(mood=mood, activity=activity)
    return render(request, 'music/generate.html', {
        'playlists': playlists,
        'mood': mood,
        'activity': activity
    })

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def landing_view(request):
    return render(request, 'music/landing.html')

from .models import UserPreferences
from django.http import JsonResponse 
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@login_required
def save_preferences(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            genres = data.get('genres', [])

            if not genres:
                return JsonResponse({'error': 'No genres provided'}, status=400)

            # Update the user's profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.preferred_genres = genres
            profile.save()

            return JsonResponse({'message': 'Preferences saved successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def match(request):
    current_user_profile = request.user.profile
    user_genres = set(current_user_profile.preferred_genres)

    # Fetch other profiles and calculate matching probability
    profiles = UserProfile.objects.exclude(user=request.user)
    matches = []

    for profile in profiles:
        other_genres = set(profile.preferred_genres)
        match_count = len(user_genres.intersection(other_genres))
        total_genres = len(user_genres.union(other_genres))
        match_percentage = (match_count / total_genres) * 100 if total_genres else 0

        matches.append({
            "username": profile.user.username,
            "bio": profile.bio,
            "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
            "match_percentage": match_percentage,
        })

    # Sort matches by the highest match percentage
    matches.sort(key=lambda x: x["match_percentage"], reverse=True)

    return render(request, "music/match.html", {"matches": matches})