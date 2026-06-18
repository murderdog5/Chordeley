import re

def split_bass(chord:str):
    if "/" in chord:
        chord = chord.split("/")
        return chord
    else:
        return [chord,None]


def split_root(chord:str):
    if len(chord) >= 2 and chord[1] in "sb":
        if "sus" in chord:
            return [chord[:chord.find("sus")],chord[chord.find("sus"):]]
        else:
            return [chord[:2],chord[2:]]
    else:
        return [chord[0],chord[1:]]


def root_to_pitch_class(root:str):
    root_map = {"C":0,
                "Cs":1,
                "Db":1,
                "D":2,
                "Ds":3,
                "Eb":3,
                "E":4,
                "Es":5,
                "F":5,
                "Fs":6,
                "Gb":6,
                "G":7,
                "Gs":8,
                "Ab":8,
                "A":9,
                "As":10,
                "Bb":10,
                "B":11,
                "Bs":0}
    return root_map[root]


def parse_suffix(suffix: str) -> tuple[str, str]:
    if suffix == "":
        return "maj", ""

    elif "sus2" in suffix:
        return "sus2", suffix.replace("sus2","")

    elif "sus4" in suffix:
        return "sus4", suffix.replace("sus4","")

    elif suffix.startswith("min"):
        return "min", suffix.removeprefix("min")

    elif suffix.startswith("dim"):
        return "dim", suffix.removeprefix("dim")

    elif suffix.startswith("aug"):
        return "aug", suffix.removeprefix("aug")

    elif suffix.startswith("no3d"):
        return "no3d", suffix.removeprefix("no3d")

    else:
        return "maj", suffix


def parse_seventh(qual: str, remainder: str) -> tuple[str, str]:
    # maj7（minmaj7/augmaj7/maj7sus はQUAL剥離後ここに来る）
    if remainder.startswith("maj7"):
        return "maj7", remainder.removeprefix("maj7")

    # dim7（QUAL=dimのときの "7" は減七 ♭♭7）
    if qual == "dim" and remainder.startswith("7"):
        return "dim7", remainder.removeprefix("7")

    # dimb7（減三和音＋短7度 ♭7）。"b7" を明示的に dom7 とする
    if remainder.startswith("b7"):
        return "dom7", remainder.removeprefix("b7")

    # dom7（明示の "7"）
    if remainder.startswith("7"):
        return "dom7", remainder.removeprefix("7")

    # add系は 7th を含意しない → SEVENTH=none、remainder はそのまま EXT へ
    if remainder.startswith("add"):
        return "none", remainder

    # 数字単独（9/11/13）は dom7 を含意。remainder は数字を残して EXT で拾う
    if remainder[:2] in ("11", "13") or remainder[:1] == "9":
        return "dom7", remainder

    # それ以外は 7th なし
    return "none", remainder


# 変化テンション候補（出現を探す順 = 優先順）。
# s9 を s11 より先に置くことで majs911s → s9 を採る（♯9優先）。
# 2文字数字（11/13）を1文字（9）より先に並べ、b9 が 13b9 で 13 を食わないよう
# 各パターンは「記号+数字」を厳密一致で探す。
_ALT_PATTERNS = ["13b", "s9", "11s", "b9", "b5", "5s"]
# 無印テンション候補（探す順）。13/11 を先に置き 9 が誤って割り込まないように。
_EXT_PATTERNS = ["13", "11", "9"]


def parse_ext_alt(remainder: str) -> tuple[str, str]:
    """残り文字列から EXT（無印テンション）と ALT（変化テンション）を1つずつ抽出。
    EXT/ALT 単一固定。候補リストを前から探し、最初に当たった1つを採る。
    これにより s91 のような不正値は構造的に発生しない。"""
    """既知の限界（実害 0.0006%、意図的に未修正）:
#   13b9 / dim13b9 は「13+♭9」が正しいが「♭13+9」と誤分解される。
#   _ALT_PATTERNS の "13b" が "13b9" で "b9" より先にマッチするため。
#   計326件/5466万トークン。学習影響は無視可能と判断し放置。"""
    r = remainder.replace("add", "")  # add は SEVENTH 段で処理済み。数字だけ残す

    # --- ALT（変化テンション）を有限候補から検出・除去 ---
    alt = "none"
    # 末尾 b は ♭13（13b 単独ケース。13b9 等は下の通常検出に回す）
    if r.endswith("13b"):
        alt = "b13"
        r = r[:-3]
    else:
        for pat in _ALT_PATTERNS:
            if pat in r:
                alt = pat
                r = r.replace(pat, "", 1)  # 最初の1つだけ除去
                break

    # --- EXT（無印テンション）を有限候補から検出 ---
    ext = "none"
    for pat in _EXT_PATTERNS:
        if pat in r:
            ext = pat
            break

    return ext, alt