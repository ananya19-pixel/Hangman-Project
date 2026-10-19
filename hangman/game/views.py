from django.shortcuts import render, redirect
import random

WORDS = [
    "internship",
    "codealpha",
    "python",
    "program",
    "security",
    "placement",
]

MAX_WRONG_GUESSES = 6


def init_game(request):
    request.session["word"] = random.choice(WORDS)
    request.session["guessed"] = []
    request.session["attempts_left"] = MAX_WRONG_GUESSES


def hangman_view(request):
    if "word" not in request.session:
        init_game(request)

    word = request.session["word"]
    guessed = request.session["guessed"]
    attempts_left = request.session["attempts_left"]

    display_word = " ".join(
        letter if letter in guessed else "_"
        for letter in word
    )

    is_won = all(letter in guessed for letter in word)
    is_lost = attempts_left <= 0

    return render(
        request,
        "game/hangman.html",
        {
            "word_display": display_word,
            "attempts_left": attempts_left,
            "is_won": is_won,
            "is_lost": is_lost,
            "guessed_letters": guessed,
            "correct_answer": word if is_lost else "",
        },
    )


def guess_letter(request):
    if request.method != "POST":
        return redirect("hangman")

    if "word" not in request.session:
        init_game(request)
        return redirect("hangman")

    letter = request.POST.get("letter", "").strip().lower()

    # Accept exactly one alphabetic letter.
    if len(letter) != 1 or not letter.isalpha():
        return redirect("hangman")

    word = request.session["word"]
    guessed = request.session["guessed"]
    attempts_left = request.session["attempts_left"]

    is_won = all(char in guessed for char in word)
    is_lost = attempts_left <= 0

    # Do not accept guesses after the game ends.
    if is_won or is_lost:
        return redirect("hangman")

    # Do not count a repeated guess twice.
    if letter not in guessed:
        guessed.append(letter)

        if letter not in word:
            attempts_left -= 1

        request.session["guessed"] = guessed
        request.session["attempts_left"] = attempts_left

    return redirect("hangman")


def restart_game(request):
    init_game(request)
    return redirect("hangman")