from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path(
        'braille-to-japanese/',
        views.braille_to_japanese,
        name='braille_to_japanese',
    ),
]
