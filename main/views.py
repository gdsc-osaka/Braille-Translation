from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def braille_to_japanese(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/braille_to_japanese.html')


def japanese_to_braille(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/japanese_to_braille.html')
