from django.urls import path
from . import views

urlpatterns = [
    path("", views.hangman_view, name="hangman"),
    path("guess/", views.guess_letter, name="guess_letter"),
    path("restart/", views.restart_game, name="restart_game"),
]