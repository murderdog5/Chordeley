"""
chord_parser の全数検算スクリプト

CHORDONOMICON で観測された全サフィックス（正常分のみ）を
parse の4ステップに通し、QUAL/SEVENTH/EXT/ALT の分解結果を一覧化する。

使い方:
  chord_parser.py と同じディレクトリに置いて実行。
  期待とズレる行を目視で探す。

注意:
  us4 / us2 / sC は split_root のバグ由来の誤切り出しなので検証対象外。
  （実データでは sus4 / sus2 として正しく parse 段に来る前提）
"""

from chord_parser import parse_suffix, parse_seventh, parse_ext_alt


def parse_suffix_full(suffix: str) -> dict:
    qual, rem = parse_suffix(suffix)
    seventh, rem = parse_seventh(qual, rem)
    ext, alt = parse_ext_alt(rem)
    return {"qual": qual, "seventh": seventh, "ext": ext, "alt": alt, "leftover": rem}


# CHORDONOMICON 観測の正常サフィックス（出現頻度つき）
SUFFIXES = [
    ("", 33771939), ("min", 11890855), ("7", 1786035), ("min7", 1329971),
    ("no3d", 730443), ("maj7", 706596), ("add9", 351456), ("sus4", 377625),
    ("sus2", 265497), ("add13", 169725), ("9", 98940), ("7sus4", 69616),
    ("dim", 61045), ("add11", 54418), ("min9", 52545), ("minadd13", 45869),
    ("dim7", 43773), ("maj9", 34737), ("aug", 22056), ("13", 21637),
    ("min11", 21497), ("11", 16167), ("7sus2", 12192), ("minadd9", 11807),
    ("minmaj7", 9272), ("7b9", 5780), ("maj7sus2", 5453), ("augmaj7", 4944),
    ("majs9", 4381), ("minadd11", 3824), ("maj13", 3288), ("maj911s", 2746),
    ("min13", 2160), ("13b", 1591), ("maj7sus4", 1137), ("maj11", 630),
    ("augmaj9", 626), ("majs911s", 408), ("dimb7", 373), ("dim9", 292),
    ("13b9", 282), ("minmaj9", 244), ("11s", 168), ("minb9", 149),
    ("maj1311s", 130), ("11b9", 95), ("dimadd13", 77), ("dim13b9", 44),
    ("dimb9", 38), ("minmaj11", 23), ("minmaj13", 12), ("min1113b", 12),
    ("dimadd11", 9), ("dim11b9", 2), ("augmaj11", 1), ("dim11", 1),
]


def main():
    print(f"{'suffix':<12}{'count':>10}  |  "
          f"{'QUAL':<7}{'SEVENTH':<9}{'EXT':<6}{'ALT':<6}{'leftover'}")
    print("-" * 78)

    flagged = []
    for suf, cnt in SUFFIXES:
        r = parse_suffix_full(suf)
        leftover = r["leftover"]
        # leftover が空でない＝何か取りこぼしている可能性。後で目視。
        mark = "  <-- leftover残り" if leftover.strip() else ""
        if leftover.strip():
            flagged.append((suf, r))
        disp = suf if suf else "(empty)"
        print(f"{disp:<12}{cnt:>10}  |  "
              f"{r['qual']:<7}{r['seventh']:<9}{r['ext']:<6}{r['alt']:<6}"
              f"{repr(leftover)}{mark}")

    print("-" * 78)
    print(f"\n取りこぼし（leftover非空）: {len(flagged)} 件")
    for suf, r in flagged:
        print(f"  {suf!r} -> {r}")

    # スロット値の種類を集計（想定外の値が出ていないか確認用）
    quals, sevenths, exts, alts = set(), set(), set(), set()
    for suf, _ in SUFFIXES:
        r = parse_suffix_full(suf)
        quals.add(r["qual"]); sevenths.add(r["seventh"])
        exts.add(r["ext"]); alts.add(r["alt"])
    print("\n--- 出現したスロット値 ---")
    print("QUAL   :", sorted(quals))
    print("SEVENTH:", sorted(sevenths))
    print("EXT    :", sorted(exts))
    print("ALT    :", sorted(alts))


if __name__ == "__main__":
    main()
