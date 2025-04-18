## This readme is ai generated

# 📄 Invoice OCR & Data Extraction App

This is a Streamlit-based web application for extracting structured data from invoice PDFs and images using OCR and AI.  
It converts invoice documents into machine-readable text with **Tesseract OCR**, and then processes the extracted text with an AI extractor to structure the data.

---

## 🚀 Features

- Upload invoices as **PDF** or **Image (PNG, JPG, JPEG)**
- Extract text from documents using **Tesseract OCR**
- Convert PDF pages to images with **poppler-utils**
- Process extracted text using an **AI-based extractor**
- Download the structured invoice data as **JSON**
- Run the app easily inside a **Docker container**

---

## 📦 Requirements

- Docker installed on your system
- A `.env` file for environment variables (if needed for AI extractor or other configs)

---

## 🐳 Docker Instructions

### 1️⃣ Build the Docker Image

```bash
docker build -t invoice-ocr-app .
```

---

### 2️⃣ Run the Docker Container

You can mount your `.env` file inside the container if required:

```bash
docker run -p 8501:8501 -v $(pwd)/.env:/app/.env invoice-ocr-app
```

OR

```bash
docker run -p 8501:8501 -v /absolute/path/to/.env:/app/.env invoice-ocr-app
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

---

## 📂 Project Structure

```
.
├── app.py               # Streamlit frontend and control logic
├── invoice_ocr.py       # Tesseract OCR and PDF-to-image functions
├── ai_extractor.py      # AI structured data extraction logic
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build instructions
├── .env                 # (Optional) environment variables
└── README.md            # Project documentation
```

---

## 📑 Example Usage

1. Open the app at [http://localhost:8501](http://localhost:8501)
2. Upload a PDF or image file containing an invoice.
3. Wait for OCR and AI processing to complete.
4. View the structured invoice data in JSON format.
5. Download the extracted data as a `.json` file.

---

## ✅ Dependencies Installed in Docker

- **Tesseract OCR** (with English language pack)
- **poppler-utils** (for PDF to image conversion)
- **Streamlit**
- **Pillow**
- **Other Python dependencies listed in `requirements.txt`**

---

## 📌 Notes

- Ensure your `.env` file has the necessary environment variables if `ai_extractor.py` or other modules rely on them.
- DPI, OCR modes, and page segmentation settings are configurable through the Streamlit sidebar.
