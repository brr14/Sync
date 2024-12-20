from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    personality_type = models.CharField(max_length=50, blank=True)
    preferred_genres = models.JSONField(default=list)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    genres = models.JSONField(default=list)  # Changed from TextField to JSONField

    def __str__(self):
        return f"Preferences for {self.user.username}"

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200)
    mood = models.CharField(max_length=50)
    activity = models.CharField(max_length=50)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    age = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'age']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Update the profile created by the signal
            user.profile.bio = self.cleaned_data.get('bio', '')
            user.profile.age = self.cleaned_data.get('age', None)
            user.profile.save()
        return user

