import streamlit as st
import database as db

#呼び出し
db.init_db()

if "root" not in st.session_state:
    st.session_state.root = None

if "progression" not in st.session_state:
    st.session_state.progression = []

if "quality" not in st.session_state:
    st.session_state.quality = None

if "tensions" not in st.session_state:
    st.session_state.tensions = []

CIRCLE = ["C","Db","D","Eb","E","F","F#","G","Ab","A","Bb","B"]

cols = st.columns(6)

for i, key in enumerate(CIRCLE):
    with cols[i % 6]:
        if st.button(key):
            st.session_state.root = key

quality = st.radio(
    "クオリティ",
    ["maj", "min", "7", "maj7", "min7", "dim", "aug", "sus4"],
    horizontal=True
)
tensions = st.multiselect(
    "テンション（任意）",
    ["9", "11", "13", "b9", "#9", "#11", "b13"]
)

tension_str = f"({','.join(tensions)})" if tensions else ""

chord = f"{st.session_state.root}{quality}{tension_str}"  if st.session_state.root else f"{quality}{tension_str}"
st.write(f"選択中コード：{chord}")

if st.button("💾コードを保存"):
    if st.session_state.root:
        st.session_state.progression.append(chord)
    else:
        st.write("エラー：ルートが選択されていません❕")

if st.button("リセット"):
    st.session_state.progression = []
if st.button("最後を取り消す") and st.session_state.progression:
    del st.session_state.progression[-1]

prog_str = f"{'→'.join(st.session_state.progression)}" if st.session_state.progression else ""
st.write(prog_str)

title = st.text_input("タイトル")
memo = st.text_area("メモ")

if len(st.session_state.progression) > 1:
    if st.button("進行を保存"):
        db.add_progression(title,prog_str,"N/A",memo,"N/A")
        st.session_state.progression = []


for i in db.get_all_progressions():
    st.write(i)