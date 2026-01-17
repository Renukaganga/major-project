import streamlit as st
import time
import cv2
import numpy as np

from modules.enhancement import enhance_image
from modules.face_detection import extract_face
from modules.embedding import get_embedding
from modules.matching import match_embedding
from db.mongodb import get_all_missing, insert_found_child


def organization_dashboard():
    st.header("🏠 Organization Dashboard – Found Child")

    uploaded_file = st.file_uploader(
        "Upload Found Child Image",
        type=["jpg", "png", "jpeg"]
    )
    location = st.text_input("Current Location")

    if uploaded_file and location and st.button("Submit"):
        with st.spinner("Processing image..."):

            start_total = time.time()

            # --------------------------------------------------
            # 0️⃣ DECODE IMAGE ONCE
            # --------------------------------------------------
            img_array = np.frombuffer(uploaded_file.read(), np.uint8)
            image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if image is None:
                st.error("Invalid image file")
                return

            # --------------------------------------------------
            # 1️⃣ FACE DETECTION FIRST (FAST)
            # --------------------------------------------------
            t0 = time.time()
            face = extract_face(image)
            st.write("⏱ Face detection:", round(time.time() - t0, 3), "sec")

            if face is None:
                st.error("❌ No face detected in the image")
                return

            # --------------------------------------------------
            # 2️⃣ CONDITIONAL ENHANCEMENT
            # --------------------------------------------------
            h, w = face.shape[:2]
            if min(h, w) < 80:
                t0 = time.time()
                face = enhance_image(face)
                st.write("⏱ Enhancement:", round(time.time() - t0, 3), "sec")
            else:
                st.write("⏱ Enhancement: skipped")

            # --------------------------------------------------
            # 3️⃣ FACE EMBEDDING
            # --------------------------------------------------
            t0 = time.time()
            embedding = get_embedding(face)
            st.write("⏱ Embedding:", round(time.time() - t0, 3), "sec")

            if embedding is None:
                st.error("❌ Could not extract face embedding")
                return

            # --------------------------------------------------
            # 4️⃣ MATCH WITH MISSING CHILD DB
            # --------------------------------------------------
            t0 = time.time()
            missing_records = get_all_missing()
            match, score = match_embedding(embedding, missing_records)
            st.write("⏱ Matching:", round(time.time() - t0, 3), "sec")

            # --------------------------------------------------
            # 5️⃣ RESULT
            # --------------------------------------------------
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

            st.write(
                "⏱ Total processing time:",
                round(time.time() - start_total, 3),
                "sec"
            )
