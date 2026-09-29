from django.test import SimpleTestCase
from django.urls import reverse


class JapaneseToBraillePageTests(SimpleTestCase):
    """japanese_to_braille.html：JSとの連携に必要な要素があること"""

    def setUp(self) -> None:
        self.response = self.client.get(reverse("main:japanese_to_braille"))

    def test_page_is_displayed(self) -> None:
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "main/japanese_to_braille.html")

    def test_page_contains_api_urls(self) -> None:
        self.assertContains(
            self.response,
            f'data-convert-url="{reverse("main:japanese_to_braille_convert")}"',
        )
        self.assertContains(
            self.response,
            f'data-reading-url="{reverse("main:japanese_to_braille_reading")}"',
        )
        self.assertContains(
            self.response,
            f'data-flip-url="{reverse("main:japanese_to_braille_flip")}"',
        )

    def test_page_contains_csrf_token(self) -> None:
        self.assertContains(self.response, 'name="csrfmiddlewaretoken"')

    def test_page_contains_elements_used_by_script(self) -> None:
        for element_id in (
            "japanese-text",
            "japanese-reading",
            "japanese-convert-button",
            "japanese-reading-edit-button",
            "braille-surface",
            "braille-output",
            "jtb-error",
        ):
            with self.subTest(element_id=element_id):
                self.assertContains(self.response, f'id="{element_id}"')

    def test_page_contains_surface_options(self) -> None:
        self.assertContains(self.response, 'value="raised"')
        self.assertContains(self.response, 'value="recessed"')

    def test_page_loads_script(self) -> None:
        self.assertContains(self.response, "main/js/japanese_to_braille.js")
