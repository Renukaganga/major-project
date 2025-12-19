# dashboards/police.py

import streamlit as st
from modules.enhancement import enhance_image
from modules.face_detection import extract_face
from modules.embedding import get_embedding
from modules.matching import match_embedding
from db.mongodb import get_all_found, insert_missing_child

def police_dashboard():
    st.header("👮 Police Dashboard – Missing Child")

    uploaded_file = st.file_uploader("Upload Missing Child Image", type=["jpg", "png", "jpeg"])
    last_seen = st.text_input("Last Seen Location")

    if uploaded_file and last_seen and st.button("Search"):
        with st.spinner("Processing image..."):
            enhanced = enhance_image(uploaded_file)
            face = extract_face(enhanced)

            if face is None:
                st.error("No face detected")
                return

            embedding = get_embedding(face)
            if embedding is None:
                st.error("Could not extract face embedding")
                return

            found_records = get_all_found()
            match, score = match_embedding(embedding, found_records)

            if match:
                st.success("✅ Match Found")
                st.write("📍 Child currently at:", match["current_location"])
                st.write("🔢 Similarity Score:", round(score, 3))
            else:
                insert_missing_child({
                    "embedding": embedding.tolist(),
                    "last_seen": last_seen
                })
                st.warning("❌ No match found. Child marked as missing.")
