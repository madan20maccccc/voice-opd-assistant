
import streamlit as st
import os
from model_utils import transcribe_audio, detect_language, translate_to_english, summarize_symptoms, generate_prescription_pdf

st.set_page_config(page_title="Voice-Based OPD Assistant", layout="centered")
st.title("🩺 Voice-Based OPD Assistant")
st.markdown("Upload a patient's voice description to generate a medical summary and prescription.")

uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
patient_name = st.text_input("Enter patient name")

if uploaded_audio and patient_name:
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_audio.read())

    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio("temp_audio.wav")
    st.success("Transcription complete")
    st.text_area("Transcribed Text", transcription)

    lang = detect_language(transcription)
    st.info(f"Detected Language: {lang}")

    if lang != 'en':
        translation = translate_to_english(transcription)
        st.text_area("Translated Text", translation)
    else:
        translation = transcription

    with st.spinner("Summarizing symptoms..."):
        summary = summarize_symptoms(translation)
    st.success("Summary ready!")
    st.text_area("Summary of Symptoms", summary)

    if st.button("Generate Prescription PDF"):
        filename = f"{patient_name.replace(' ', '_')}_prescription.pdf"
        filepath = generate_prescription_pdf(patient_name, summary, filename)
        with open(filepath, "rb") as f:
            st.download_button(label="Download Prescription", data=f, file_name=filename)
