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

tunagi_flag = False
english_flag = 0    # 外字符の時１、外国語引用符の時２
gaijifu_flag = False
large_flag = 0      # 大文字符1個の時１（次の一文字のみ大文字）、2個の時２（次のスペースまで全て大文字）
numeric_flag = False
youon_flag = False
dakuon_flag = False
handakuon_flag = False
alphabet_small = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
alphabet_large = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
seion = ["カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ツ", "テ", "ト", "ハ", "ヒ", "フ", "ヘ", "ホ"]
dakuon =["ガ", "ギ", "グ", "ゲ", "ゴ", "ザ", "ジ", "ズ", "ゼ", "ゾ", "ダ", "ヂ", "ヅ", "デ", "ド", "バ", "ビ", "ブ", "ベ", "ボ"]
handakuon = ["パ", "ピ", "プ", "ペ", "ポ"]
youon = ["ャ", "ュ", "ョ", "ァ", "ィ", "ゥ", "ェ", "ォ"]
youon_pattern = len(youon)
tyokuon = "" 
return_text = ""

# 変換用関数

def get_index(li, value):
    try:
        return li.index(value)
    except ValueError:
        return None

# 英語の処理
def english_converter(data, text):
    # 大文字の処理
    if data["english"] == "大文字符":
        large_flag += 1
    elif large_flag > 0:
        index_number = get_index(alphabet_small, data["english"])
        if index_number is not None:
            text += alphabet_large[index_number]
            if large_flag == 1:
                large_flag = 0
    # 大文字以外の処理
    else:
        if data["english"] == "数符":
            numeric = True
        elif data["english"] == "カッコ":
            if tunagi_flag:
                text += ")"
                tunagi_flag = False
            else:
                text += "("
                tunagi_flag = False
        elif data["english"] == "外国語引用符終わり":
            english_flag = 0
            large_flag = 0
        elif data["english"] == " " and english_flag == 1:
            english_flag = 0
            large_flag = 0
        else: 
            text += data["english"]
    return text

# 日本語の処理
def japanese_converter(dots_key, data, text):
    if data["japanese"] == "数符":
        numeric = True
    # 「外字符」と「、」の処理(同じ点字のためスペースの有無で判断)
    elif data["japanese"] == "、":
        gaijifu_flag = 1
    elif gaijifu_flag == 1 and data["japanese"] = "　":
        gaijifu_flag = 0
        text += "、　"
    elif data["japanese"] == "第1カッコ":
        if tunagi_flag = 1:
            tunagi_flag = 0
            text += "）"
        else:
            text += "（"
    elif data["japanese"] == "第一つなぎ符":
        text += "-"
    elif data["japanese"] == "外国語引用符始まり":
        english_flag = 2
    elif data["japanese"] == "外国語引用符終わり":
        english_flag = 0

    elif data["japanese"] == "拗音符":
        youon_flag = True
    elif data["japanese"] == "濁点符":
        dakuon_flag = True
    elif data["japanese"] == "半濁点符":
        handakuon_flag = True
    elif data["japanese"] == "濁点符と拗音符":
        youon_flag = True
        dakuon_flag = True
    elif data["japanese"] == "半濁点符と拗音符":
        youon_flag = True
        handakuon_flag = True

    # 拗音の処理 
    elif youon_flag:
        youon_flag = False
        if dots_key[0] == 1 and dots_key[1] == 0 and dots_key[3] == 0:   # 例：きゃ
            youon_pattern = 0
            tyokuon = DOTS_LOOKUP.get([1, 1, dots_key[2], 0, dots_key[4], dots_key[5]]) 
        elif dots_key[0] == 1 and dots_key[1] == 0 and dots_key[3] == 1: # 例：きゅ
            youon_pattern = 1
            tyokuon = DOTS_LOOKUP.get([1, 1, dots_key[2], 0, dots_key[4], dots_key[5]])
        elif dots_key[0] == 0 and dots_key[1] == 1 and dots_key[3] == 1: # 例：きょ
            youon_pattern = 2
            tyokuon = DOTS_LOOKUP.get([1, 1, dots_key[2], 0, dots_key[4], dots_key[5]])
        elif dots_key[0] == 1 and dots_key[1] == 1 and dots_key[3] == 0: # 例：すぃ
            youon_pattern = 4
            tyokuon = DOTS_LOOKUP.get([1, 0, dots_key[2], 1, dots_key[4], dots_key[5]])
        elif dots_key[0] == 1 and dots_key[1] == 1 and dots_key[3] == 1: # 例：きぇ
            youon_pattern = 6
            tyokuon = DOTS_LOOKUP.get([1, 1, dots_key[2], 0, dots_key[4], dots_key[5]])
        # 濁った拗音などの処理（例：ぎゃ、ぴゃ）
        if dakuon_flag:
            dakuon_flag = False
            index_number = get_index(seion, tyokuon)
            if index_number is not None:
                tyokuon = dakuon[index_number]
        if handakuon_flag:
            handakuon_flag = False
            index_number = get_index(seion, tyokuon)
            if index_number is not None and index_number >= 15:
                tyokuon = handakuon[(index_number % 5)]
            
        if youon_pattern <= 7:
            text = text + tyokuon + youon[youon_pattern]
        tyokuon = ""
        youon = len(youon)

    # 濁音、半濁音の処理
    elif dakuon_flag:
        dakuon_flag = False
        index_number = get_index(seion, data["japanese"])
        if index_number is not None:
            text += dakuon[index_number]
    elif handakuon_flag:
        handakuon_flag = False
        index_number = get_index(seion, data["japanese"])
        if index_number is not None and index_number >= 15:
            text += handakuon[(index_number % 5)]
    
    else:
        text += data["japanese"]

    return text


def convert_dots_to_text(dots: list[list[int]]) -> str:
    for dots_list in dots:
        dot_key = tuple(dots_list)
        
        # 検索テーブルからデータを取得
        entry = DOTS_LOOKUP.get(dot_key)

        if entry:
            if numeric_flag:
                if entry["numeric"] != "":
                    return_text += entry["numeric"]
            else:
                numeric_flag = False
                # 英語の処理
                if english_flag > 0:
                    english_converter(entry, return_text)

                # 日本語の処理      
                else:
                    japanese_converter(dot_key, entry, return_text)
    return return_text