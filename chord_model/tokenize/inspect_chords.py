"""
Chordonomicon データ中身チェック用スクリプト

目的:
  生のコード表記にどんなユニーク要素が含まれるかを洗い出し、
  設計のすり合わせができる形でファイルに書き出す。

確認する観点:
  1. <...> 形式の構造注釈（<verse_1> 等）の全種類
  2. コード表記そのもののユニーク一覧（出現頻度つき）
  3. 根音部分のユニーク一覧（シャープが # か s か、b はどうか）
  4. ベース（/以降）のユニーク一覧
  5. サフィックス（根音とベースを除いた部分）のユニーク一覧

出力:
  chord_inspection.txt （人が読む用サマリ）
  chord_inspection.json（プログラムで再利用する用）
"""

from datasets import load_dataset
import re
import collections
import json


def split_bass(token: str):
    """'/' でベースを切り離す。なければ bass=None。"""
    if "/" in token:
        body, bass = token.split("/", 1)
        return body, bass
    return token, None


def split_root_rough(body: str):
    """
    根音を大まかに切り出す（確認用なので寛容に）。
    先頭の英字1つ + 続く # / b / s をまとめて根音候補とみなす。
    """
    m = re.match(r"^([A-Ga-g][#bs]?)(.*)$", body)
    if m:
        return m.group(1), m.group(2)
    return None, body  # 英字始まりでない異常ケース


def main():
    print("loading dataset ...")
    ds = load_dataset("ailsntua/Chordonomicon")
    df = ds["train"].to_pandas()

    annotation_counter = collections.Counter()   # <...> 形式
    chord_counter = collections.Counter()        # コード表記まるごと
    root_counter = collections.Counter()         # 根音部分
    bass_counter = collections.Counter()         # ベース部分
    suffix_counter = collections.Counter()       # サフィックス部分

    n_rows = 0
    n_tokens = 0

    for row in df["chords"]:
        n_rows += 1
        for tok in row.split():
            n_tokens += 1

            # 構造注釈かどうか
            if re.fullmatch(r"<.*?>", tok):
                annotation_counter[tok] += 1
                continue

            chord_counter[tok] += 1

            body, bass = split_bass(tok)
            if bass is not None:
                bass_counter[bass] += 1

            root, suffix = split_root_rough(body)
            if root is not None:
                root_counter[root] += 1
            suffix_counter[suffix] += 1

    # ---- サマリをテキストで書き出す ----
    lines = []
    lines.append("=== CHORDONOMICON 中身チェック ===")
    lines.append(f"曲数(行数): {n_rows}")
    lines.append(f"総トークン数: {n_tokens}")
    lines.append("")

    lines.append(f"--- 1. 構造注釈 <...> の種類: {len(annotation_counter)} ---")
    for k, v in annotation_counter.most_common():
        lines.append(f"  {k}\t{v}")
    lines.append("")

    lines.append(f"--- 2. 根音(root)のユニーク: {len(root_counter)} ---")
    lines.append("  （シャープが # か s か、b 表記かをここで確認）")
    for k, v in sorted(root_counter.items(), key=lambda x: -x[1]):
        lines.append(f"  {repr(k)}\t{v}")
    lines.append("")

    lines.append(f"--- 3. ベース(/以降)のユニーク: {len(bass_counter)} ---")
    for k, v in sorted(bass_counter.items(), key=lambda x: -x[1]):
        lines.append(f"  {repr(k)}\t{v}")
    lines.append("")

    lines.append(f"--- 4. サフィックスのユニーク: {len(suffix_counter)} ---")
    for k, v in sorted(suffix_counter.items(), key=lambda x: -x[1]):
        lines.append(f"  {repr(k)}\t{v}")
    lines.append("")

    lines.append(f"--- 5. コード表記まるごとのユニーク: {len(chord_counter)} ---")
    lines.append("  （上位100件のみ表示）")
    for k, v in chord_counter.most_common(100):
        lines.append(f"  {k}\t{v}")
    lines.append("")

    with open("chord_inspection.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # ---- 再利用用に JSON でも書き出す ----
    out = {
        "n_rows": n_rows,
        "n_tokens": n_tokens,
        "annotations": dict(annotation_counter.most_common()),
        "roots": dict(sorted(root_counter.items(), key=lambda x: -x[1])),
        "basses": dict(sorted(bass_counter.items(), key=lambda x: -x[1])),
        "suffixes": dict(sorted(suffix_counter.items(), key=lambda x: -x[1])),
        "chords_top200": dict(chord_counter.most_common(200)),
    }
    with open("chord_inspection.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("done. -> chord_inspection.txt / chord_inspection.json")


if __name__ == "__main__":
    main()
