from django import forms
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from main.converter_libkuraji import (
    convert_braille_to_kana,
    convert_kana,
    convert_kanji,
    flip_dots,
)
from main.japanese_to_braille_forms import (
    BrailleTextForm,
    JapaneseTextForm,
    KanaReadingForm,
)


def _error_response(form: forms.Form, field: str) -> JsonResponse:
    errors = form.errors.get(field)
    message = str(errors[0]) if errors else "入力内容を確認してください。"
    return JsonResponse({"error": message}, status=400)


@require_POST
def convert_japanese_to_braille(request: HttpRequest) -> JsonResponse:
    """「変換」：文章 → 点字（convert_kanji）→ 読み（convert_braille_to_kana）。"""
    form = JapaneseTextForm(request.POST)

    if not form.is_valid():
        return _error_response(form, "text")

    braille = convert_kanji(form.cleaned_data["text"])
    reading = convert_braille_to_kana(braille)
    return JsonResponse({"braille": braille, "reading": reading})


@require_POST
def convert_reading_to_braille(request: HttpRequest) -> JsonResponse:
    """「修正」：読み → 点字（convert_kana）。"""
    form = KanaReadingForm(request.POST)

    if not form.is_valid():
        return _error_response(form, "reading")

    braille = convert_kana(form.cleaned_data["reading"])
    return JsonResponse({"braille": braille})


@require_POST
def flip_braille(request: HttpRequest) -> JsonResponse:
    """表示面の切り替え：点字 → 反転した点字（flip_dots）。"""
    form = BrailleTextForm(request.POST)

    if not form.is_valid():
        return _error_response(form, "braille")

    braille = flip_dots(form.cleaned_data["braille"])
    return JsonResponse({"braille": braille})
