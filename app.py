import streamlit as st

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

chord = f"{st.session_state.root}{quality}{tension_str}"



st.write(tensions)
st.write(quality)
st.write("選択中：", st.session_state.selected)