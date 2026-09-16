import json

from django.test import SimpleTestCase
from django.urls import reverse


class BrailleToJapaneseApiTests(SimpleTestCase):
    def setUp(self) -> None:
        self.url = reverse("main:braille_to_japanese_convert")

    def test_converts_valid_braille_dots(self) -> None:
        response = self.client.post(
            self.url,
            data={"dots": json.dumps([[1, 0, 0, 0, 0, 0]])},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": "ア"})

    def test_returns_bad_request_for_invalid_dots(self) -> None:
        response = self.client.post(
            self.url,
            data={"dots": "[[1, 0, 2, 0, 0, 0]]"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "各点は0または1で指定してください。"},
        )

    def test_returns_bad_request_when_dots_are_missing(self) -> None:
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "点字を1文字以上入力してください。"},
        )

    def test_rejects_get_requests(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
