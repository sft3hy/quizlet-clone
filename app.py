import streamlit as st
import pandas as pd
from PIL import Image
import os
import random

st.set_page_config(page_title="Flashcard App", layout="centered")
st.title("📚 Not Quizlet")

CSV_PATH = "cards.csv"
IMG_FOLDER = "img"

# Load and validate CSV
if not os.path.exists(CSV_PATH):
    st.error(f"CSV file not found at: {CSV_PATH}")
else:
    df_original = pd.read_csv(CSV_PATH)
    required_cols = {"term", "definition", "filename"}

    if not required_cols.issubset(df_original.columns):
        st.error(f"CSV must contain columns: {', '.join(required_cols)}")
    else:
        # Shuffle deck once or reshuffle if requested
        if "shuffled_df" not in st.session_state or st.button("🔀 Shuffle Deck"):
            st.session_state.shuffled_df = df_original.sample(frac=1).reset_index(
                drop=True
            )
            st.session_state.index = 0
            st.session_state.flipped = False

        df = st.session_state.shuffled_df

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️ Prev"):
                st.session_state.index = max(0, st.session_state.index - 1)
                st.session_state.flipped = False
        with col2:
            if st.button("🔄 Flip"):
                st.session_state.flipped = not st.session_state.flipped
        with col3:
            if st.button("➡️ Next"):
                st.session_state.index = min(len(df) - 1, st.session_state.index + 1)
                st.session_state.flipped = False

        # Flashcard content
        card = df.iloc[st.session_state.index]
        term = card["term"]
        definition = card["definition"]
        image_filename = card["filename"]

        st.markdown("### Flashcard")

        if not st.session_state.flipped:
            st.success(f"**Definition:**\n\n{definition}")

            # Only attempt to load and display image if valid filename exists
            if isinstance(image_filename, str) and image_filename.strip():
                image_path = os.path.join(IMG_FOLDER, image_filename.strip())
                if os.path.exists(image_path):
                    st.image(Image.open(image_path))
        else:
            st.info(f"**Term:** {term}")

        st.markdown(f"Card {st.session_state.index + 1} of {len(df)}")
