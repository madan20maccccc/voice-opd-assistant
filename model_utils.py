
import whisper
from langdetect import detect
# Replace:
# from googletrans import Translator

# With:
from deep_translator import GoogleTranslator

def translate_to_english(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

from transformers import pipeline
from fpdf import FPDF
import os

model = whisper.load_model("base")
summarizer = pipeline("summarization", model="t5-small")

from pydub import AudioSegment
import whisper
import os

model = whisper.load_model("base")

def transcribe_audio(audio_path):
    # Convert to WAV in 16kHz mono (Whisper needs this)
    converted_path = "converted_whisper.wav"
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(converted_path, format="wav")

    # Transcribe using Whisper
    result = model.transcribe(converted_path)
    os.remove(converted_path)
    return result["text"]


def detect_language(text):
    return detect(text)

def translate_to_english(text):
    translator = Translator()
    translated = translator.translate(text, dest='en')
    return translated.text

def summarize_symptoms(text):
    summary = summarizer(text, max_length=60, min_length=10, do_sample=False)
    return summary[0]['summary_text']

def generate_prescription_pdf(patient_name, summary_text, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="OPD Prescription", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Patient Name: {patient_name}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Summary: {summary_text}")
    if not os.path.exists("prescriptions"):
        os.mkdir("prescriptions")
    pdf.output(f"prescriptions/{file_name}")
    return f"prescriptions/{file_name}"
