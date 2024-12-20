from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.main_view, name='main'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('landing/', views.landing_view, name='landing'),
    path('personality/', views.personality_quiz_view, name='personality_quiz'),
    path('generate/', views.generate_playlist_view, name='generate_playlist'),
    path('profile/',views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('save-preferences/', views.save_preferences, name='save_preferences'),
    path('match/', views.match, name='match'),
]