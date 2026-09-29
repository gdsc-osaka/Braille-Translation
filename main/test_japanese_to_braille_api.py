from django.test import Client, SimpleTestCase
from django.urls import reverse

from main.converter_libkuraji import (
    convert_braille_to_kana,
    convert_kana,
    convert_kanji,
    flip_dots,
)
from main.japanese_to_braille_forms import MAX_TEXT_LENGTH


class ConvertJapaneseToBrailleApiTests(SimpleTestCase):
    """「変換」ボタン：convert_kanji → convert_braille_to_kana"""

    def setUp(self) -> None:
        self.url = reverse("main:japanese_to_braille_convert")

    def test_returns_braille_and_reading(self) -> None:
        text = "今日は良い天気です。"
        response = self.client.post(self.url, data={"text": text})

        braille = convert_kanji(text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"braille": braille, "reading": convert_braille_to_kana(braille)},
        )

    def test_reading_keeps_sentence_end_kuten(self) -> None:
        response = self.client.post(self.url, data={"text": "今日は良い天気です。"})

        self.assertTrue(response.json()["reading"].endswith("。"))

    def test_empty_text(self) -> None:
        response = self.client.post(self.url, data={"text": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"braille": "", "reading": ""})

    def test_missing_text_is_treated_as_empty(self) -> None:
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"braille": "", "reading": ""})

    def test_returns_bad_request_for_too_long_text(self) -> None:
        response = self.client.post(
            self.url,
            data={"text": "あ" * (MAX_TEXT_LENGTH + 1)},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": f"文章は{MAX_TEXT_LENGTH}文字以内で入力してください。"},
        )

    def test_rejects_get_requests(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)


class ConvertReadingToBrailleApiTests(SimpleTestCase):
    """「修正」ボタン：convert_kana"""

    def setUp(self) -> None:
        self.url = reverse("main:japanese_to_braille_reading")

    def test_returns_braille(self) -> None:
        reading = "キョーワ　ヨイ　テンキデス。"
        response = self.client.post(self.url, data={"reading": reading})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"braille": convert_kana(reading)})

    def test_empty_reading(self) -> None:
        response = self.client.post(self.url, data={"reading": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"braille": ""})

    def test_returns_bad_request_for_too_long_reading(self) -> None:
        response = self.client.post(
            self.url,
            data={"reading": "ア" * (MAX_TEXT_LENGTH + 1)},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": f"読みは{MAX_TEXT_LENGTH}文字以内で入力してください。"},
        )

    def test_rejects_get_requests(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)


class FlipBrailleApiTests(SimpleTestCase):
    """凸面（表面）⇔凹面（裏面）の切り替え：flip_dots"""

    def setUp(self) -> None:
        self.url = reverse("main:japanese_to_braille_flip")

    def test_returns_flipped_braille(self) -> None:
        braille = "⠈⠪⠒⠄ ⠜⠃ ⠟⠴⠣⠐⠟⠹⠲"
        response = self.client.post(self.url, data={"braille": braille})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"braille": flip_dots(braille)})

    def test_flipping_twice_returns_original(self) -> None:
        braille = "⠈⠪⠒⠄ ⠜⠃ ⠠⠩"
        first = self.client.post(self.url, data={"braille": braille}).json()
        second = self.client.post(
            self.url,
            data={"braille": first["braille"]},
        ).json()

        self.assertEqual(second, {"braille": braille})

    def test_hiragana_reading_can_be_flipped(self) -> None:
        """「修正」でひらがなが□になった点字も切り替えられること"""
        braille = self.client.post(
            reverse("main:japanese_to_braille_reading"),
            data={"reading": "きょーわ"},
        ).json()["braille"]

        response = self.client.post(self.url, data={"braille": braille})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"braille": flip_dots(braille)})

    def test_returns_bad_request_for_non_braille(self) -> None:
        response = self.client.post(self.url, data={"braille": "abc"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "点字データに対応していない文字が含まれています。"},
        )

    def test_rejects_get_requests(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)


class JapaneseToBrailleCsrfTests(SimpleTestCase):
    """CSRFトークンが無いPOSTは拒否されること"""

    def test_requires_csrf_token(self) -> None:
        client = Client(enforce_csrf_checks=True)

        for name, data in (
            ("main:japanese_to_braille_convert", {"text": "あ"}),
            ("main:japanese_to_braille_reading", {"reading": "ア"}),
            ("main:japanese_to_braille_flip", {"braille": "⠁"}),
        ):
            with self.subTest(url=name):
                response = client.post(reverse(name), data=data)

                self.assertEqual(response.status_code, 403)
