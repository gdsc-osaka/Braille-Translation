from django.test import SimpleTestCase
from django.urls import reverse


class BrailleToJapanesePageIntegrationTests(SimpleTestCase):
    def test_page_contains_keyboard_input_form(self) -> None:
        response = self.client.get(reverse("main:braille_to_japanese"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'action="{reverse("main:braille_to_japanese_convert")}"',
        )
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'data-dot-number="1"')
        self.assertContains(response, "数字キーの1から6で点を切り替え")
        self.assertContains(response, "Enterキーで次のセルへ進みます。")
        self.assertContains(response, "左右キーでセルを移動できます。")
        self.assertContains(response, "main/js/braille_to_japanese.js")
