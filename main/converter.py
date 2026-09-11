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

numeric_flag = False
# english: 外字符の時１、外国語引用符の時２
# large: 大文字符1個の時１（次の一文字のみ大文字）、2個の時２（次のスペースまで全て大文字）
alphabet_small = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
flag_list = {'english': 0, 'large': 0 'toten': False, 'gimonfu': False, 'kuten': False, 'tunagi': False, 'youon': False, 'dakuon': False, 'handakuon': False, 'tokushu': False}
alphabet_large = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
seion = ["カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ツ", "テ", "ト", "ハ", "ヒ", "フ", "ヘ", "ホ", "ウ"]
dakuon =["ガ", "ギ", "グ", "ゲ", "ゴ", "ザ", "ジ", "ズ", "ゼ", "ゾ", "ダ", "ヂ", "ヅ", "デ", "ド", "バ", "ビ", "ブ", "ベ", "ボ", "ヴ"]
handakuon = ["パ", "ピ", "プ", "ペ", "ポ"]
youon = ["ャ", "ュ", "ョ", "ァ", "ィ", "ゥ", "ェ", "ォ"]
youon_pattern = len(youon)

# 変換用関数

def get_index(li, value):
    try:
        return li.index(value)
    except ValueError:
        return None

# 英語の処理
def english_converter(data, sikibetu):
    text = ""
    # アルファベット以外の処理
    if data["english"] == "数符":
        numeric_flag = True
    elif data["english"] == "カッコ":
        if sikibetu.get("tunagi"):
            text += ")"
            sikibetu["tunagi"] = False
        else:
            text += "("
            sikibetu["tunagi"] = True
    elif data["english"] == "外国語引用符終わり":
        sikibetu["english"] = 0
        sikibetu["large"] = 0
    elif data["english"] == " " and sikibetu.get("english") == 1:
        text += " "
        sikibetu["english"] = 0
        sikibetu["large"] = 0

    elif data["english"] == "大文字符":
        sikibetu["large"] += 1
    # 大文字の処理
    elif sikibetu.get("large") > 0:
        index_number = get_index(alphabet_small, data["english"])
        if index_number is not None:
            text += alphabet_large[index_number]
            if sikibetu.get("large") == 1:
                sikibetu["large"] = 0
        # ピリオド等のアルファベット以外の文字の対応
        elif data["english"] != "":
            text += data["english"]
        else:
            text += "■"
    # 大文字以外の処理
    if text == "":
        if data["english"] != "":
            text += data["english"]
        else:
            text += "■"
    return text, sikibetu

# 日本語の処理
def japanese_converter(dots_key, data, sikibetu):
    text = ""
    tyokuon = ""
    if data["japanese"] == "数符":
        numeric_flag = True
    # 「外字符」と「、」の処理(同じ点字のためスペースの有無で判断)
    elif data["japanese"] == "、":
        sikibetu["toten"] = True
    elif sikibetu.get("toten") == True:
        sikibetu["toten"] = False
        if data["japanese"] == "　":
            sikibetu["toten"]
            text += "、　"
        elif data["japanese"] == "ネ":
            text += "％"
        elif data["japanese"] == "ヘ":
            text += "＆"
        elif data["japanese"] == "コ":
            text += "＠"
        elif data["japanese"] == "ク":
            text += "＃"
        elif data["japanese"] == "カ":
            text += "＊"
    elif data["japanese"] == "第1カッコ":
        if sikibetu.get("tunagi"):
            text += "）"
            sikibetu["tunagi"] = False
        else:
            text += "（"
            sikibetu["sikibetu"] = True
    elif data["japanese"] == "第一つなぎ符":
        text += "-"
    elif data["japanese"] == "外国語引用符始まり":
        sikibetu["english"] = 2
    elif data["japanese"] == "外国語引用符終わり":
        sikibetu["english"] = 0

    elif data["japanese"] == "？":
        sikibetu["gimonfu"] = True
    elif sikibetu.get("gimonfu") == True and data["japanese"] == "　":
        sikibetu["gimonfu"] = False
        text += "？　"
    elif data["japanese"] == "。":
        sikibetu["kuten"] = True
    elif sikibetu.get("kuten") == True and data["japanese"] == "　":
        sikibetu["kuten"] = False
        text += "。　"

    elif data["japanese"] == "拗音符":
        sikibetu["youon"] = True
    elif data["japanese"] == "濁点符":
        sikibetu["dakuon"] = True
    elif data["japanese"] == "半濁点符":
        sikibetu["handakuon"] = True
    elif data["japanese"] == "濁点符と拗音符":
        sikibetu["youon"] = True
        sikibetu["dakuon"] = True
    elif data["japanese"] == "半濁点符と拗音符":
        sikibetu["youon"] = True
        sikibetu["handakuon"] = True

    # 拗音符の処理 
    elif sikibetu.get("youon"):
        sikibetu["youon"] = False
        if dots_key[0] == 1 and dots_key[1] == 0 and dots_key[3] == 0:   # 例：きゃ
            youon_pattern = 0
            tyokuon = DOTS_LOOKUP.get((1, 1, dots_key[2], 0, dots_key[4], dots_key[5]))["japanese"] 
        elif dots_key[0] == 1 and dots_key[1] == 0 and dots_key[3] == 1: # 例：きゅ
            youon_pattern = 1
            tyokuon = DOTS_LOOKUP.get((1, 1, dots_key[2], 0, dots_key[4], dots_key[5]))["japanese"]
        elif dots_key[0] == 0 and dots_key[1] == 1 and dots_key[3] == 1: # 例：きょ
            youon_pattern = 2
            tyokuon = DOTS_LOOKUP.get((1, 1, dots_key[2], 0, dots_key[4], dots_key[5]))["japanese"]
        elif dots_key[0] == 1 and dots_key[1] == 1 and dots_key[3] == 0: # 例：すぃ"、てぃ
            youon_pattern = 4
            if data["japanese"] == "シ":
                tyokuon = "ス"
            elif data["japanese"] == "チ":
                tyokuon = "テ"
        elif dots_key[0] == 1 and dots_key[1] == 1 and dots_key[3] == 1: # 例：きぇ
            youon_pattern = 6
            tyokuon = DOTS_LOOKUP.get((1, 1, dots_key[2], 0, dots_key[4], dots_key[5]))["japanese"]
        # 濁った拗音などの処理（例：ぎゃ、ぴゃ）
        if sikibetu.get("dakuon"):
            sikibetu["dakuon"] = False
            index_number = get_index(seion, tyokuon)
            if index_number is not None:
                tyokuon = dakuon[index_number]
        if sikibetu.get("handakuon"):
            sikibetu["handakuon"] = False
            if data["japanese"] == "ツ":
                text += "テュ"
            elif data["japanese"] == "ユ":
                text += "フュ"
            elif data["japanese"] == "ヨ":
                text += "フョ"
            else:
                index_number = get_index(seion, tyokuon)
                if index_number is not None and index_number >= 15:
                    tyokuon = handakuon[(index_number % 5)]
            
        if youon_pattern <= 7:
            text = text + tyokuon + youon[youon_pattern]
        tyokuon = ""
        youon = len(youon)
    
    # 特殊音の処理（拗音符、濁点符、半濁点符以外のもの）
    elif sikibetu.get("gimonfu") or sikibetu.get("kuten"):
        if dots_key[0] == 1 and dots_key[1] == 0 and dots_key[3] == 0:   # 例：くぁ
            youon_pattern = 3
        elif dots_key[0] == 1 and dots_key[1] == 1 and dots_key[3] == 0: # 例：くぃ
            youon_pattern = 4
        elif dots_key[0] == 1 and dots_key[1] == 1 and dots_key[3] == 1: # 例：くぇ
            youon_pattern = 6
        elif dots_key[0] == 0 and dots_key[1] == 1 and dots_key[3] == 0: # 例：くぉ
            youon_pattern = 7
        tyokuon = DOTS_LOOKUP.get((1, 0, dots_key[2], 1, dots_key[4], dots_key[5]))["japanese"]
        if dots_key[0] == 1 and dots_key[1] == 0 and dots_key[3] == 1:   # 例：とぅ
            youon_pattern = 5
            if sikibetu.get("gimonfu"):
                tyokuon = "と"
            elif sikibetu.get("kuten"):
                tyokuon = "ど"
                sikibetu["kuten"] = False
        elif sikibetu.get("kuten"):
            if dots_key[2] == 1 and dots_key[4] == 0 and dots_key[5] == 1:
                tyokuon = "ヴ"
            else:
                index_number = get_index(seion, tyokuon)
                if index_number is not None:
                    tyokuon = dakuon[index_number]
            sikibetu["kuten"] = False
        sikibetu["gimonfu"] = False
        if youon_pattern <= 7:
            text = text + tyokuon + youon[youon_pattern]
        tyokuon = ""
        youon = len(youon)
    elif dots_key == (0, 0, 0, 1, 1, 1):
        sikibetu["tokushu"] = True
    elif sikibetu.get("tokushu"):
        if dots_key == (1, 0, 1, 1, 1, 0):
            text += "デュ"
        elif dots_key == (0, 0, 1, 1, 0, 1):
            text += "ヴュ"
        elif dots_key == (0, 0, 1, 1, 1, 0):
            text += "ヴョ"
        sikibetu["tokushu"] = False

    # 濁音符、半濁音符の処理
    elif sikibetu.get("dakuon"):
        sikibetu["dakuon"] = False
        if dots_key == (1, 0, 1, 0, 1, 1):
            text += "〇"
        elif dots_key == (1, 1, 1, 0, 1, 1):
            text += "△"
        elif dots_key == (1, 0, 1, 1, 1, 1):
            text += "□"
        elif dots_key == (1, 1, 1, 1, 1, 1):
            text += "×"
        else:
            index_number = get_index(seion, data["japanese"])
            if index_number is not None:
                text += dakuon[index_number]
    elif sikibetu.get("handakuon"):
        sikibetu["handakuon"] = False
        index_number = get_index(seion, data["japanese"])
        if index_number is not None and index_number >= 15:
            text += handakuon[(index_number % 5)]
    
    if text == "" and data["japanese"] != "":
        text += data["japanese"]
    else:
        text += "■"

    return text, sikibetu


def convert_dots_to_text(dots: list[list[int]]) -> str:
    return_text = ""
    for dots_list in dots:
        dot_key = tuple(dots_list)
        
        # 検索テーブルからデータを取得
        entry = DOTS_LOOKUP.get(dot_key)

        if entry:
            if numeric_flag and entry["numeric"] != "":
                    return_text += entry["numeric"]
            else:
                numeric_flag = False
                # 英語の処理
                if english_flag > 0:
                    texts, english_flag = english_converter(entry, flag_list)
                    return_text += texts

                # 日本語の処理      
                else:
                    texts, english_flag = japanese_converter(dot_key, entry, flag_list)
                    return_text += texts
        else:
            return_text += "　"
    return return_text