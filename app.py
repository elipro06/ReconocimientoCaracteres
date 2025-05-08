import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
import os

st.set_page_config(page_title="Texto a Voz - OCR", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }

    h1 {
        color: #1A73E8 !important;
        text-align: center;
        font-family: 'Verdana', sans-serif;
        font-size: 2.5em;
    }

    .stButton > button, .stCameraInput, .stRadio > div {
        background-color: #1A73E8 !important;
        color: white !important;
        border-radius: 6px;
        border: none;
        font-weight: bold;
    }

    .stSidebar {
        background-color: #f0f2f6 !important;
    }

    .stSidebar div, .stSidebar label, .stSidebar span {
        color: #1A1A1A !important;
    }

    .css-1offfwp, .css-1aumxhk {
        color: #1A1A1A !important;
    }

    .stMarkdown {
        font-family: 'Helvetica', sans-serif;
        font-size: 1.1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📸 Texto a Voz desde una Imagen")

st.markdown("Haz una foto con texto y te mostraremos el texto extraído junto con su audio.")

img_file_buffer = st.camera_input("Captura una imagen con texto")

with st.sidebar:
    apply_filter = st.radio("¿Aplicar filtro blanco y negro a la imagen?", ('Sí', 'No'))

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if apply_filter == 'Sí':
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    st.image(img_rgb, caption="Imagen cargada", use_column_width=True)

    extracted_text = pytesseract.image_to_string(img_rgb)
    st.subheader("📝 Texto Detectado:")
    st.write(extracted_text)

    if extracted_text.strip() != "":
        tts = gTTS(extracted_text, lang='es')
        audio_path = "audio_output.mp3"
        tts.save(audio_path)

        st.subheader("🔊 Reproducir Audio:")
        audio_file = open(audio_path, "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        audio_file.close()
        os.remove(audio_path)
    else:
        st.error("No se detectó texto en la imagen. Intenta con una imagen más nítida.")
