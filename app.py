import spacy
from spacy.cli import download

# Download the small English model if it’s not installed
download("en_core_web_sm")

# Load the model so we can use it
nlp = spacy.load("en_core_web_sm")
import streamlit 
as st
import pandas as pd
import spacy
from fuzzywuzzy import fuzz

# Load hymn Excel
df = pd.read_excel("CCDM Song selection 2025.xlsx")

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Extract themes
def extract_themes(text):
    doc = nlp(text)
    return list(set([token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]]))

# Match hymns
def match_hymns(themes, df, top_n=5, fuzzy_threshold=60):
    matches = []
    for idx, row in df.iterrows():
        hymn_keywords = str(row.get('Theme/Notes', '')).lower().split(",")
        score = sum(fuzz.partial_ratio(t, kw.strip()) >= fuzzy_threshold for t in themes for kw in hymn_keywords)
        if score > 0:
            matches.append((row['Song Title'], row['Composer'], score))
    matches.sort(key=lambda x: x[2], reverse=True)
    return matches[:top_n]

# Streamlit UI
st.title("AI Hymn Assistant")
reading_text = st.text_area("Paste the readings of the day here:")

if st.button("Get Hymn Suggestions"):
    if reading_text.strip():
        themes = extract_themes(reading_text)
        st.write("**Extracted Themes:**", themes)
        suggestions = match_hymns(themes, df)
        if suggestions:
            st.write("### Suggested Hymns")
            for i, (title, composer, score) in enumerate(suggestions, 1):
                st.write(f"{i}. {title} by {composer} (Score: {score})")
        else:
            st.write("No hymns matched the readings.")
    else:
        st.warning("Please paste the readings first.")
