import streamlit as st
import pandas as pd
import spacy
from fuzzywuzzy import fuzz
import subprocess
import sys

# Load spaCy model (install if missing)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
    ])
    nlp = spacy.load("en_core_web_sm")

# Load Excel file with hymns
df = pd.read_excel("CCDM Song Selection 2025.xlsx")

st.title("AI Hymn Assistant")
st.write("Paste the readings below, and get hymn suggestions:")

# Input readings
readings_input = st.text_area("Readings", placeholder="Paste your readings here...", height=200)

if st.button("Get Hymn Suggestions"):
    if not readings_input.strip():
        st.warning("Please enter the readings first!")
    else:
        # Preprocess readings
        readings_doc = nlp(readings_input.lower())
        readings_text = " ".join([token.lemma_ for token in readings_doc if not token.is_stop])

        # Score hymns
        hymn_scores = []
        for index, row in df.iterrows():
            hymn_text = str(row["Hymn Text"]).lower()
            score = fuzz.partial_ratio(readings_text, hymn_text)
            hymn_scores.append((row["Hymn Name"], score))

        # Sort by score descending
        hymn_scores.sort(key=lambda x: x[1], reverse=True)

        # Display top 5 suggestions
        st.subheader("Top Hymn Suggestions")
        for hymn, score in hymn_scores[:5]:
            st.write(f"**{hymn}** – Match Score: {score}")
