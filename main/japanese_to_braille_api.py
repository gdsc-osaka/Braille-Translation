import logging
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

logger = logging.getLogger(__name__)


def _error_response(form: forms.Form, field: str) -> JsonResponse:
    errors = form.errors.get(field)
    message = str(errors[0]) if errors else "入力内容を確認してください。"
    return JsonResponse({"error": message}, status=400)


@require_POST
def convert_japanese_to_braille(request: HttpRequest) -> JsonResponse:
    """「変換」：文章 → 点字（convert_kanji）→ 読み（convert_braille_to_kana）。"""
    logger.info("Japanese-to-braille API: request received")

    try:
        form = JapaneseTextForm(request.POST)

        if not form.is_valid():
            logger.warning("Japanese-to-braille API: invalid form")
            return _error_response(form, "text")

        logger.info("Japanese-to-braille API: starting convert_kanji")
        braille = convert_kanji(form.cleaned_data["text"])
        logger.info("Japanese-to-braille API: convert_kanji completed")

        reading = convert_braille_to_kana(braille)
        logger.info("Japanese-to-braille API: reading conversion completed")

        return JsonResponse({"braille": braille, "reading": reading})

    except Exception:
        logger.exception("Japanese-to-braille API: unexpected error")
        return JsonResponse(
            {"error": "文章を変換できませんでした。"},
            status=500,
        )


@require_POST
def convert_reading_to_braille(request: HttpRequest) -> JsonResponse:
    """「修正」：読み → 点字（convert_kana）。"""
    try:
        form = KanaReadingForm(request.POST)

        if not form.is_valid():
            return _error_response(form, "reading")

        braille = convert_kana(form.cleaned_data["reading"])
        return JsonResponse({"braille": braille})

    except Exception:
        logger.exception("Reading-to-braille API: unexpected error")
        return JsonResponse(
            {"error": "読みを点字に変換できませんでした。"},
            status=500,
        )


@require_POST
def flip_braille(request: HttpRequest) -> JsonResponse:
    """表示面の切り替え：点字 → 反転した点字（flip_dots）。"""
    try:
        form = BrailleTextForm(request.POST)

        if not form.is_valid():
            return _error_response(form, "braille")

        braille = flip_dots(form.cleaned_data["braille"])
        return JsonResponse({"braille": braille})

    except Exception:
        logger.exception("Braille flip API: unexpected error")
        return JsonResponse(
            {"error": "表示面を切り替えられませんでした。"},
            status=500,
        )