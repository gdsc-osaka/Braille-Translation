import json

from django.test import SimpleTestCase

from main.forms import BrailleDotsForm


class BrailleDotsFormTests(SimpleTestCase):
    def test_accepts_valid_braille_cells(self) -> None:
        dots = [
            [1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 1],
        ]
        form = BrailleDotsForm(data={"dots": json.dumps(dots)})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["dots"], dots)

    def test_rejects_invalid_json(self) -> None:
        form = BrailleDotsForm(data={"dots": "not-json"})

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "dots",
            "点字データの形式が正しくありません。",
        )

    def test_rejects_empty_cells(self) -> None:
        form = BrailleDotsForm(data={"dots": "[]"})

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "dots",
            "点字を1文字以上入力してください。",
        )

    def test_rejects_cell_without_six_dots(self) -> None:
        form = BrailleDotsForm(data={"dots": "[[1, 0, 0]]"})

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "dots",
            "点字1文字は6個の点で指定してください。",
        )

    def test_rejects_values_other_than_zero_or_one(self) -> None:
        form = BrailleDotsForm(data={"dots": "[[1, 0, 2, 0, 0, 0]]"})

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "dots",
            "各点は0または1で指定してください。",
        )

    def test_rejects_boolean_values(self) -> None:
        form = BrailleDotsForm(data={"dots": "[[true, 0, 0, 0, 0, 0]]"})

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "dots",
            "各点は0または1で指定してください。",
        )
