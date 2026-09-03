from django.test import TestCase
from django.urls import reverse


class BrailleToJapanesePageTests(TestCase):
    def test_page_is_displayed(self) -> None:
        response = self.client.get(reverse('main:braille_to_japanese'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/braille_to_japanese.html')
        self.assertContains(response, '点字から日本語への変換')
