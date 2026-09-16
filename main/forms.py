import json
from typing import cast

from django import forms


BRAILLE_DOT_COUNT = 6


class BrailleDotsForm(forms.Form):
    dots = forms.CharField(
        widget=forms.HiddenInput,
        error_messages={
            "required": "点字を1文字以上入力してください。",
        },
    )

    def clean_dots(self) -> list[list[int]]:
        raw_dots: str = self.cleaned_data["dots"]

        try:
            parsed_dots: object = json.loads(raw_dots)
        except json.JSONDecodeError as error:
            raise forms.ValidationError(
                "点字データの形式が正しくありません。",
                code="invalid_json",
            ) from error

        if not isinstance(parsed_dots, list):
            raise forms.ValidationError(
                "点字データの形式が正しくありません。",
                code="invalid_structure",
            )

        if not parsed_dots:
            raise forms.ValidationError(
                "点字を1文字以上入力してください。",
                code="empty",
            )

        validated_dots: list[list[int]] = []

        for cell in parsed_dots:
            if not isinstance(cell, list) or len(cell) != BRAILLE_DOT_COUNT:
                raise forms.ValidationError(
                    "点字1文字は6個の点で指定してください。",
                    code="invalid_cell",
                )

            if any(
                not isinstance(dot, int)
                or isinstance(dot, bool)
                or dot not in (0, 1)
                for dot in cell
            ):
                raise forms.ValidationError(
                    "各点は0または1で指定してください。",
                    code="invalid_dot",
                )

            validated_dots.append(cell.copy())

        return validated_dots

    def get_validated_dots(self) -> list[list[int]]:
        if not self.is_bound or not self.is_valid():
            raise ValueError("検証済みの点字データを取得できません。")

        return cast(list[list[int]], self.cleaned_data["dots"])
