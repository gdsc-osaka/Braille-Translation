from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def braille_to_japanese(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/braille_to_japanese.html')
