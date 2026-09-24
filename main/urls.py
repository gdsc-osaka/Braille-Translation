from django.urls import path

from . import views
from .braille_to_japanese_api import convert_braille_to_japanese

app_name = 'main'

urlpatterns = [
    path(
        'japanese-to-braille/',
        views.japanese_to_braille,
        name='japanese_to_braille',
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
