from django.test import SimpleTestCase

from main.japanese_to_braille_forms import (
    MAX_TEXT_LENGTH,
    BrailleTextForm,
    JapaneseTextForm,
    KanaReadingForm,
)


class JapaneseTextFormTests(SimpleTestCase):
    def test_accepts_text(self) -> None:
        form = JapaneseTextForm(data={"text": "今日は良い天気です。"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["text"], "今日は良い天気です。")

    def test_accepts_empty_text(self) -> None:
        form = JapaneseTextForm(data={"text": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["text"], "")

    def test_keeps_surrounding_whitespace(self) -> None:
        form = JapaneseTextForm(data={"text": " あ\n"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["text"], " あ\n")

    def test_rejects_too_long_text(self) -> None:
        form = JapaneseTextForm(data={"text": "あ" * (MAX_TEXT_LENGTH + 1)})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["text"],
            [f"文章は{MAX_TEXT_LENGTH}文字以内で入力してください。"],
        )


class KanaReadingFormTests(SimpleTestCase):
    def test_accepts_reading(self) -> None:
        form = KanaReadingForm(data={"reading": "キョーワ　ヨイ　テンキデス。"})

        self.assertTrue(form.is_valid())

    def test_accepts_empty_reading(self) -> None:
        form = KanaReadingForm(data={"reading": ""})

        self.assertTrue(form.is_valid())

    def test_rejects_too_long_reading(self) -> None:
        form = KanaReadingForm(data={"reading": "ア" * (MAX_TEXT_LENGTH + 1)})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["reading"],
            [f"読みは{MAX_TEXT_LENGTH}文字以内で入力してください。"],
        )


class BrailleTextFormTests(SimpleTestCase):
    def test_accepts_braille_and_space(self) -> None:
        form = BrailleTextForm(data={"braille": "⠈⠪⠒⠄ ⠜⠃"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["braille"], "⠈⠪⠒⠄ ⠜⠃")

    def test_accepts_unconvertible_mark(self) -> None:
        form = BrailleTextForm(data={"braille": "□□⠒□"})

        self.assertTrue(form.is_valid())

    def test_accepts_empty_braille(self) -> None:
        form = BrailleTextForm(data={"braille": ""})

        self.assertTrue(form.is_valid())

    def test_rejects_non_braille_characters(self) -> None:
        for braille in ("abc", "あ", "⠁\n⠁", "■", "⡀"):
            with self.subTest(braille=braille):
                form = BrailleTextForm(data={"braille": braille})

                self.assertFalse(form.is_valid())
                self.assertEqual(
                    form.errors["braille"],
                    ["点字データに対応していない文字が含まれています。"],
                )

    def test_rejects_too_long_braille(self) -> None:
        form = BrailleTextForm(data={"braille": "⠁" * (MAX_TEXT_LENGTH + 1)})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["braille"],
            [f"点字は{MAX_TEXT_LENGTH}文字以内にしてください。"],
        )
