import pytesseract
import re
import streamlit as st
import os
from pdf2image import convert_from_path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def clean(s):
    text = re.sub(r"[^\w\s\.\,\-\&\$]","",s)
    text = re.sub(r"\n\s*\n","\n\n",text)
    text = re.sub(r"(\w)\n(\w)",r"\1 \2",text)
    text = re.sub(r"\s+"," ",text).strip()
    return text

def extract(pdf_path):
    pages = convert_from_path(pdf_path)
    sections = {}
    for i in pages:
        i = pytesseract.image_to_string(i).split('\n\n')
        feature,content = clean(i[0]).strip(),clean(' '.join(i[1:])).strip()
        sections[feature] = content
    return sections

from google import genai

client = genai.Client(api_key="AIzaSyDAKVVIa51EoGUT0U-76-r_5eYRgcSzdOs")

def analyze(sections):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"The given dictionary is a pitch deck of a company, you have to analyze each key sections and assign weights based on the importance of different sections. Generate a pitch score (0-100) based on predefined metrics. Provide personalized feedback on which areas need improvement and mention some points in the given dictionary. Only display pitch score + generated feedback(<=100 words). Sections dictionry:{sections}"
    )
    return response.text

st.title("Pitch Deck Analyzer")

file = st.file_uploader("Upload PDF", type=["pdf"])

if file:
    with open("temp.pdf", "wb") as f:
        f.write(file.read())
    st.info("Extracting text...")
    sections = extract("temp.pdf")

    if sections:
        st.success("Text extracted successfully! Analyzing pitch...")
        result = analyze(sections)
        st.subheader("Pitch Score & Feedback")
        st.write(result)
    else:
        st.error("Failed to extract text. Try another PDF.")
    os.remove("temp.pdf")