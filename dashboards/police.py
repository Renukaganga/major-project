import streamlit as st
import time
import cv2
import numpy as np

from modules.enhancement import enhance_image
from modules.face_detection import extract_face
from modules.embedding import get_embedding
from modules.matching import match_embedding
from db.mongodb import get_all_found, insert_missing_child


def police_dashboard():
    st.header("👮 Police Dashboard – Missing Child")

    uploaded_file = st.file_uploader(
        "Upload Missing Child Image",
        type=["jpg", "png", "jpeg"]
    )
    last_seen = st.text_input("Last Seen Location")

    if uploaded_file and last_seen and st.button("Search"):
        with st.spinner("Processing image..."):

            start_total = time.time()

            # --------------------------------------------------
            # 0️⃣ DECODE IMAGE ONCE (VERY IMPORTANT)
            # --------------------------------------------------
            img_array = np.frombuffer(uploaded_file.read(), np.uint8)
            image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if image is None:
                st.error("Invalid image file")
                return

            # --------------------------------------------------
            # 1️⃣ FACE DETECTION (NOW RECEIVES NUMPY IMAGE ✅)
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

            # --------------------------------------------------
            # 4️⃣ MATCHING
            # --------------------------------------------------
            t0 = time.time()
            found_records = get_all_found()
            match, score = match_embedding(embedding, found_records)
            st.write("⏱ Matching:", round(time.time() - t0, 3), "sec")

            # --------------------------------------------------
            # 5️⃣ RESULT
            # --------------------------------------------------
            if match:
                st.success("✅ Match Found")
                st.write("📍 Current Location:", match["current_location"])
                st.write("🔢 Similarity Score:", round(score, 3))
            else:
                insert_missing_child({
                    "embedding": embedding.tolist(),
                    "last_seen": last_seen
                })
                st.warning("❌ No match found. Child marked as missing.")

            st.write(
                "⏱ Total processing time:",
                round(time.time() - start_total, 3),
                "sec"
            )
