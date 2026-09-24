import libkuraji
import json
from pathlib import Path
from . import converter

# JSONファイルの絶対パスを取得
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "braille_data.json"

# ファイルの読み込み
with open(DATA_PATH, "r", encoding="utf-8") as f:
    BRAILLE_DATASET = json.load(f)

UNICODE_TO_DOTS_ARRAY = {item["unicode"]: item["dots_array"] for item in BRAILLE_DATASET}
UNICODE_TO_UNICODE_FLIPPED = {item["unicode"]: item["unicode_flipped"] for item in BRAILLE_DATASET}

def convert_kanji(text):
    if text == "":
        return ""
    else:
        braille, in_pos, out_pos, cursor = libkuraji.translate_kanji(
            text,
            unicodeIO=True,
        )
        return braille

def convert_kana(text):
    return libkuraji.translate(text)

def convert_braille_to_kana(cell: str) -> str:
    cell_split = list(cell)
    dot_list = []
    for i in cell_split:
        dot_list.append(UNICODE_TO_DOTS_ARRAY.get(i, [0, 0, 0, 0, 0, 0]))
    return converter.convert_dots_to_text(dot_list)

def flip_dots(cell: str) -> str:
    cell_reversed = list(cell)[::-1]
    dots_list = []
    for i in cell_reversed:
        if i == "□":
            dots_list.append(i)
        else:
            dots_list.append(UNICODE_TO_UNICODE_FLIPPED.get(i, [0, 0, 0, 0, 0, 0]))
    return "".join(dots_list)