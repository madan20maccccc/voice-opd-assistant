import streamlit as st
import tempfile
import os
from model_utils import (
    transcribe_audio,
    detect_language,
    translate_to_english,
    summarize_symptoms,
    generate_prescription_pdf,
)

st.set_page_config(page_title="Voice-Based OPD Assistant", layout="centered")
st.title("🩺 Voice-Based OPD Assistant")
st.markdown("Upload a patient's voice description to generate a medical summary and prescription.")

uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
patient_name = st.text_input("Enter patient name")

if uploaded_audio and patient_name:
    # Save uploaded file to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(uploaded_audio.read())
        temp_audio_path = temp_file.name

    # Transcribe the audio
    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio(temp_audio_path)
    st.success("✅ Transcription complete")
    st.text_area("📝 Transcribed Text", transcription)

    # Detect language
    lang = detect_language(transcription)
    st.info(f"🌐 Detected Language: `{lang}`")

    # Translate if not English
    if lang != 'en':
        translation = translate_to_english(transcription)
        st.text_area("🔁 Translated Text (to English)", translation)
    else:
        translation = transcription

    # Summarize symptoms
    with st.spinner("Summarizing symptoms..."):
        summary = summarize_symptoms(translation)
    st.success("✅ Summary ready!")
    st.text_area("📋 Summary of Symptoms", summary)

    # Generate prescription
    if st.button("🧾 Generate Prescription PDF"):
        filename = f"{patient_name.replace(' ', '_')}_prescription.pdf"
        filepath = generate_prescription_pdf(patient_name, summary, filename)

        with open(filepath, "rb") as f:
            st.download_button(
                label="📥 Download Prescription",
                data=f,
                file_name=filename,
                mime='application/pdf'
            )
