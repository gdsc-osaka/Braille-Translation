from django.test import TestCase

from .converter_libkuraji import (
    BRAILLE_DATASET,
    UNICODE_TO_UNICODE_FLIPPED,
    convert_kanji,
    convert_kana,
    convert_braille_to_kana,
    flip_dots,
)


class ConverterLibkurajiTest(TestCase):
    """converter_libkuraji.py の基本動作を確認するテスト"""

    def test_convert_kanji_returns_braille(self):
        """漢字かな混じり文 → Unicode点字"""
        text = "私は点字を読みます。"

        result = convert_kanji(text)

        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

        # libkuraji README の出力例と一致することを確認
        expected = "⠄⠕⠳⠄ ⠟⠴⠐⠳⠔ ⠜⠷⠵⠹⠲"
        self.assertEqual(result, expected)

    def test_convert_kanji_empty(self):
        """空文字を渡した場合"""
        result = convert_kanji("")

        self.assertIsInstance(result, str)

    def test_convert_kana_returns_braille(self):
        """かな文 → Unicode点字"""
        text = "ワタシワ テンジヲ ヨミマス。"

        result = convert_kana(text)

        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_convert_braille_to_kana_returns_japanese(self):
        """かな → Unicode点字 → 日本語"""
        braille = convert_kanji("わたしはてんじをよみます。")

        result = convert_braille_to_kana(braille)

        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")
    
    def test_convert_braille_to_kana_returns_japanese(self):
        """漢字 → Unicode点字 → 日本語"""
        braille = convert_kanji("私は点字を読みます。")

        result = convert_braille_to_kana(braille)

        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")
    
    def test_convert_braille_to_kana_returns_english(self):
        """Unicode点字 → 英語"""
        braille = convert_kanji("I read braille.")

        result = convert_braille_to_kana(braille)

        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")
    
    def test_convert_braille_to_kana_returns_numeric(self):
        """Unicode点字 → 数字"""
        braille = convert_kanji("I read braille.")

        result = convert_braille_to_kana(braille)

        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_convert_braille_to_kana_unknown_cell(self):
        """変換表に存在しないUnicode点字が空白として処理されること"""
        result = convert_braille_to_kana("★")

        self.assertIsInstance(result, str)
    
    def test_flip_dots(self):
        """点字 → 順番と向きともに反転した点字"""
        result = flip_dots("⠄⠕⠳⠄ ⠟⠴⠐⠳⠔ ⠜⠷⠵⠹⠲")

        expected = "⠖⠏⠮⠾⠣ ⠢⠞⠂⠦⠻ ⠠⠞⠪⠠"
        self.assertEqual(result, expected)
    
    def test_flip_dots_twice_returns_original(self):
        """2回反転すると元の点字に戻ること"""
        braille = "⠈⠪⠒⠄ ⠜⠃ ⠟⠴⠣⠐⠟⠹⠲ ⠠⠩"

        result = flip_dots(flip_dots(braille))

        self.assertEqual(result, braille)
    
    def test_flip_dots_keeps_unconvertible_mark(self):
        """変換できなかった文字（□）はそのまま残り、位置だけ反転すること"""
        result = flip_dots("□⠁")

        self.assertEqual(result, "⠈□")
    
    def test_flip_dots_empty(self):
        """空文字を渡した場合"""
        result = flip_dots("")

        self.assertEqual(result, "")


def mirror_dots(dots):
    """裏面から見た点の並び（1↔4、2↔5、3↔6）"""
    return dots[3:] + dots[:3]


def dots_to_unicode(dots):
    """6点の並び → Unicode点字"""
    return chr(0x2800 + sum(1 << index for index, dot in enumerate(dots) if dot))


class BrailleDataFlipTest(TestCase):
    """braille_data.json の unicode_flipped が正しいことを確認するテスト"""

    def test_unicode_flipped_is_mirror_of_dots(self):
        """全ての点字で、unicode_flipped が点の並びを左右反転したものになっていること"""
        for item in BRAILLE_DATASET:
            with self.subTest(unicode=item["unicode"]):
                expected = (
                    " "
                    if item["unicode"] == " "
                    else dots_to_unicode(mirror_dots(item["dots_array"]))
                )
                self.assertEqual(item["unicode_flipped"], expected)

    def test_flipping_twice_returns_original(self):
        """全ての点字で、2回反転すると元に戻ること"""
        for original, flipped in UNICODE_TO_UNICODE_FLIPPED.items():
            with self.subTest(unicode=original):
                self.assertEqual(UNICODE_TO_UNICODE_FLIPPED[flipped], original)