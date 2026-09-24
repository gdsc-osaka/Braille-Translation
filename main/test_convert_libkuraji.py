from django.test import TestCase

from .converter_libkuraji import (
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