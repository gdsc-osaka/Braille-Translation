import json
from pathlib import Path

# JSONファイルの絶対パスを取得
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "braille_data.json"

# ファイルの読み込み
with open(DATA_PATH, "r", encoding="utf-8") as f:
    BRAILLE_DATASET = json.load(f)

# 高速検索用の辞書（インデックス）作成、各種変数定義
DOTS_LOOKUP = {
    tuple(item["dots_array"]): item
    for item in BRAILLE_DATASET
}

tunagi_flag = 0
english_flag = 0
gaijifu_flag = 0
large_flag = 0
numeric_flag = 0
alphabet_small = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
alphabet_large = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
seion = ["カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ツ", "テ", "ト", "ハ", "ヒ", "フ", "ヘ", "ホ"]
dakuon =["ガ", "ギ", "グ", "ゲ", "ゴ", "ザ", "ジ", "ズ", "ゼ", "ゾ", "ダ", "ヂ", "ヅ", "デ", "ド", "バ", "ビ", "ブ", "ベ", "ボ"]
handakuon = ["パ", "ピ", "プ", "ペ", "ポ"]
return_text = ""

# 変換用関数

def convert_dots_to_japanese(dots_list: list[int]) -> str:

    dots_key = tuple(dots_list)
    
    # 検索テーブルからデータを取得
    entry = DOTS_LOOKUP.get(dots_key)

    if entry:
        return entry["japanese"]
    return ""  # 不正な入力の場合は空文字