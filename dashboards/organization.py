# dashboards/organization.py

import streamlit as st
from modules.enhancement import enhance_image
from modules.face_detection import extract_face
from modules.embedding import get_embedding
from modules.matching import match_embedding
from db.mongodb import get_all_missing, insert_found_child

def organization_dashboard():
    st.header("🏠 Organization Dashboard – Found Child")

    uploaded_file = st.file_uploader("Upload Found Child Image", type=["jpg", "png", "jpeg"])
    location = st.text_input("Current Location")

    if uploaded_file and location and st.button("Submit"):
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

            missing_records = get_all_missing()
            match, score = match_embedding(embedding, missing_records)

            if match:
                st.success("✅ Match Found")
                st.write("🚓 Police notified")
                st.write("🔢 Similarity Score:", round(score, 3))
            else:
                insert_found_child({
                    "embedding": embedding.tolist(),
                    "current_location": location
                })
                st.warning("❌ No match found. Child stored as found.")
