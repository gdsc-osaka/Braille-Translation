from django import forms

from main.converter_libkuraji import UNICODE_TO_UNICODE_FLIPPED


MAX_TEXT_LENGTH = 5000


class JapaneseTextForm(forms.Form):
    """「変換」ボタン用：文章を入力のテキスト。"""

    text = forms.CharField(
        required=False,
        strip=False,
        max_length=MAX_TEXT_LENGTH,
        error_messages={
            "max_length": f"文章は{MAX_TEXT_LENGTH}文字以内で入力してください。",
        },
    )


class KanaReadingForm(forms.Form):
    """「修正」ボタン用：読みのテキスト。"""

    reading = forms.CharField(
        required=False,
        strip=False,
        max_length=MAX_TEXT_LENGTH,
        error_messages={
            "max_length": f"読みは{MAX_TEXT_LENGTH}文字以内で入力してください。",
        },
    )


class BrailleTextForm(forms.Form):
    """表示面の切り替え用：点字の文字列。"""

    braille = forms.CharField(
        required=False,
        strip=False,
        max_length=MAX_TEXT_LENGTH,
        error_messages={
            "max_length": f"点字は{MAX_TEXT_LENGTH}文字以内にしてください。",
        },
    )

    def clean_braille(self) -> str:
        braille: str = self.cleaned_data["braille"]

        # flip_dots が対応していない文字（6点点字・空白・□以外）は受け付けない
        if any(
            char not in UNICODE_TO_UNICODE_FLIPPED and char not in ("□",)
            for char in braille
        ):
            raise forms.ValidationError(
                "点字データに対応していない文字が含まれています。",
                code="invalid_braille",
            )

        return braille
