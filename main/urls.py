from django.urls import path

from . import views
from .braille_to_japanese_api import convert_braille_to_japanese
from .japanese_to_braille_api import (
    convert_japanese_to_braille,
    convert_reading_to_braille,
    flip_braille,
)

app_name = 'main'

urlpatterns = [
    path(
        'japanese-to-braille/',
        views.japanese_to_braille,
        name='japanese_to_braille',
    ),
    path(
        'japanese-to-braille/convert/',
        convert_japanese_to_braille,
        name='japanese_to_braille_convert',
    ),
    path(
        'japanese-to-braille/reading/',
        convert_reading_to_braille,
        name='japanese_to_braille_reading',
    ),
    path(
        'japanese-to-braille/flip/',
        flip_braille,
        name='japanese_to_braille_flip',
    ),
    path(
        'braille-to-japanese/',
        views.braille_to_japanese,
        name='braille_to_japanese',
    ),
    path(
        'braille-to-japanese/convert/',
        convert_braille_to_japanese,
        name='braille_to_japanese_convert',
    ),
]
