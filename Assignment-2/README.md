# **Pitch Deck Analyzer**  
**Analyze startup pitch decks using AI & OCR**  

## **Overview**  
The **Pitch Deck Analyzer** extracts text from a PDF pitch deck, cleans and structures the data, and uses Google’s **Gemini API** to analyze key sections. It assigns a **pitch score (0-100)** and provides **personalized feedback** on areas for improvement.  

---

## **Methodology**  

### **1. PDF Text Extraction (OCR)**  
- The application uses **`pdf2image`** to **convert** PDF pages into images.  
- **`pytesseract`** (Tesseract OCR) extracts text from each image.  
- Extracted text is **segmented into sections** based on formatting.  

### **2. Text Cleaning & Preprocessing**  
- The extracted text often contains **unwanted characters, extra spaces, and line breaks**.  
- I used **regular expressions (`re`)** to:  
  - Remove **special characters**.  
  - Fix **broken words** split across lines.  
  - Normalize **whitespace**.  

### **3. Structuring Data into Sections**  
- Each page is processed into **key-value pairs** where:  
  - **Key** = Likely a **section title** (`"Problem"`, `"Solution"`).  
  - **Value** = The **corresponding content** under that section.  
  - Key (heading of a page) and Value (content of page) were separated by '\n\n'. This helped me to differentiate between them.
- This helps **Gemini AI** understand the structure of the pitch deck.  

### **4. AI-Powered Pitch Analysis**  
- The cleaned **sections dictionary** is sent to **Google Gemini API (`gemini-2.0-flash`)**.  
- The AI **evaluates** each section based on predefined criteria.  
- **Output:**  
  - **Pitch Score (0-100)** based on content quality.  
  - **Feedback (≤100 words)** suggesting improvements.  

---

## **Installation & Setup**  

### **1. Install Dependencies**  
Ensure you have Python **3.8+** installed. Then, run:  
```sh  
pip install -r requirements.txt  
```

### **2. Install Tesseract OCR**  
- **Windows:** Download and install from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki).   
---

## **How to Run**  

### **1. Start the Streamlit App**  
Run this command in your terminal:  
```sh
streamlit run main.py  
```

### **2. Upload a Pitch Deck PDF**  
- Click **"Browse files"** and select a **PDF pitch deck**.  
- The app will **extract, clean, and analyze** the text.  

### **3. View the Results**  
- The **Pitch Score** (0-100) is displayed.  
- **Feedback** on how to improve the pitch deck is shown.  

---

## **File Structure**  
```
Assignment-2
│── Data                   # Datasets Directory
    │── pdfs              
│── main.py                # Main Streamlit application
│── Code.ipynb             # Notebook
│── requirements.txt       # Required dependencies
│── README.md              # This documentation
```
## Author
Developed by **Karthikeya**.