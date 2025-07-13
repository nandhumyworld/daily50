# Day 10/50 - AI Python Challenge
# Name List : Store 5 names in a list and print them with their lengths.
# Use filename as NameList.py

import streamlit as st
import pandas as pd

# Title
st.title("Name Length Analyzer")

# --- Initialize session state for names ---
if "names" not in st.session_state:
    st.session_state.names = [""] * 5

# --- Reset function ---
def reset_app():
    st.session_state.names = [""] * 5
    st.rerun()

# --- Input boxes ---
for i in range(5):
    st.session_state.names[i] = st.text_input(
        f"Enter Name {i+1}",
        value=st.session_state.names[i],
        key=f"name_{i}"
    )

# --- Measure Length ---
if st.button("Measure Length"):
    valid_names = [name for name in st.session_state.names if name.strip()]
    
    if not valid_names:
        st.warning("Please enter at least one valid name.")
    else:
        df = pd.DataFrame({
            "Name": valid_names,
            "Length": [len(name) for name in valid_names]
        })
        st.subheader("Name Lengths")
        st.bar_chart(df.set_index("Name"))

# --- Reset button ---
if st.button("Reset"):
    reset_app()
