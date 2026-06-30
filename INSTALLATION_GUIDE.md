# 📦 Installation Guide - Multi-Format Support

## Pengenalan

Panduan ini untuk install semua dependencies yang diperlukan untuk mendukung multi-format processing (PDF, DOC, EXCEL, CSV, TXT).

---

## 📋 Prerequisites

- Python 3.8 atau lebih baru
- pip package manager
- Virtual environment (recommended)

---

## 🚀 Quick Installation

### Langkah 1: Install Core Dependencies
```bash
pip install -r requirements.txt
```

### Langkah 2: Install Format-Specific Tools

#### untuk PDF Support (OCR)
```bash
# Install pytesseract & pdf2image
pip install pytesseract pdf2image

# Download & install Tesseract-OCR dari:
# https://github.com/UB-Mannheim/tesseract/wiki

# Download & install Poppler dari:
# https://github.com/oschwartz10612/poppler-windows/releases/
```

#### Untuk DOCX Support
```bash
pip install python-docx
```

#### Untuk Excel Support
```bash
pip install openpyxl
```

### Langkah 3: Verify Installation
```bash
# Test semua imports
python -c "
import fastapi
import langchain
import faiss
print('✅ Core packages OK')

try:
    import docx
    print('✅ DOCX support OK')
except:
    print('⚠️ DOCX support NOT installed')

try:
    import openpyxl
    print('✅ EXCEL support OK')
except:
    print('⚠️ EXCEL support NOT installed')

try:
    import pytesseract
    print('✅ PDF support OK')
except:
    print('⚠️ PDF support NOT installed')
"
```

---

## 🔧 Detailed Installation by OS

### Windows 10/11

#### 1. Core Packages (Required)
```powershell
pip install -r requirements.txt
```

#### 2. PDF Support Installation
```powershell
# Install Python packages
pip install pytesseract pdf2image Pillow

# Download Tesseract-OCR
# Go to: https://github.com/UB-Mannheim/tesseract/wiki
# Download: tesseract-ocr-w64-setup-v5.x.exe (latest version)
# Install to: C:\Program Files\Tesseract-OCR

# Download Poppler
# Go to: https://github.com/oschwartz10612/poppler-windows/releases/
# Download: Release-25.12.0 (latest)
# Extract to: C:\poppler\

# Verify Tesseract installation
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

#### 3. DOCX Support Installation
```powershell
pip install python-docx
```

#### 4. EXCEL Support Installation
```powershell
pip install openpyxl
```

#### 5. Verify All
```powershell
# Test import
python -c "
from docx import Document
from openpyxl import load_workbook
from pdf2image import convert_from_path
import pytesseract
print('✅ All packages installed successfully')
"
```

---

### macOS

#### 1. Install Tesseract via Homebrew
```bash
brew install tesseract
brew install poppler
```

#### 2. Install Python Packages
```bash
pip install -r requirements.txt
pip install python-docx openpyxl pytesseract pdf2image Pillow
```

#### 3. Verify
```bash
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
```

---

### Linux (Ubuntu/Debian)

#### 1. Install System Dependencies
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

#### 2. Install Python Packages
```bash
pip install -r requirements.txt
pip install python-docx openpyxl pytesseract pdf2image Pillow
```

#### 3. Verify
```bash
which tesseract
which pdfimages
```

---

## ✅ Verification Checklist

### Test Setiap Format

```python
# test_formats.py
import os

# Test TXT
with open('test.txt', 'w') as f:
    f.write("Test content")
print("✅ TXT support")

# Test CSV
import csv
with open('test.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['A', 'B', 'C'])
print("✅ CSV support")

# Test DOCX
try:
    from docx import Document
    doc = Document()
    print("✅ DOCX support")
except Exception as e:
    print(f"❌ DOCX error: {e}")

# Test EXCEL
try:
    import openpyxl
    wb = openpyxl.Workbook()
    print("✅ EXCEL support")
except Exception as e:
    print(f"❌ EXCEL error: {e}")

# Test PDF
try:
    from pdf2image import convert_from_path
    import pytesseract
    print("✅ PDF support")
except Exception as e:
    print(f"❌ PDF error: {e}")
```

Run verification:
```bash
python test_formats.py
```

---

## 🆘 Troubleshooting

### PDF Not Working

**Error**: `pytesseract.TesseractNotFoundError`

**Solution**:
```python
# Add to chat_api.py
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### PDF Images Not Converting

**Error**: `PDFPageCounterror` or `pop filename issue`

**Solution**: Install poppler
```bash
# Windows
# Download from: https://github.com/oschwartz10612/poppler-windows/releases/

# Or update chat_api.py poppler_path:
poppler_path = r"C:\\poppler\\poppler-25.12.0\\Library\\bin"
```

### DOCX Import Error

**Error**: `ModuleNotFoundError: No module named 'docx'`

**Solution**:
```bash
pip install python-docx
```

### Excel File Error

**Error**: `zipfile.BadZipFile` or similar

**Solution**:
```bash
pip install --upgrade openpyxl
```

### CSV Encoding Error

**Error**: `UnicodeDecodeError`

**Solution**: Save CSV as UTF-8
```bash
# On Windows
# Excel → Save As → CSV UTF-8 (.csv)

# Or convert using Python
import pandas as pd
df = pd.read_csv('file.csv', encoding='latin-1')
df.to_csv('file_utf8.csv', encoding='utf-8')
```

---

## 🧪 Test Environment Setup

Create isolated test environment:

```bash
# Create virtual environment
python -m venv multiformat_env

# Activate
# Windows:
multiformat_env\Scripts\activate
# macOS/Linux:
source multiformat_env/bin/activate

# Install requirements
pip install -r requirements.txt

# Test
python test_multiformat.py
```

---

## 📊 Minimal vs Full Installation

### Minimal (TXT + CSV only)
```bash
pip install fastapi uvicorn langchain python-dotenv mysql-connector-python
```

### Medium (+ PDF Support)
```bash
pip install -r requirements.txt
pip install pytesseract pdf2image
# Install Tesseract & Poppler separately
```

### Full (All Formats)
```bash
pip install -r requirements.txt
pip install python-docx openpyxl pytesseract pdf2image
# Install Tesseract & Poppler separately
```

---

## 🎯 Quick Test After Installation

```bash
# 1. Start API
uvicorn chat_api:app --reload

# 2. Test upload TXT
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@documents/test.txt"

# 3. Check status
curl http://localhost:8000/vectorstore-status

# 4. Test chat
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}'
```

---

## 📝 Notes

- **Optional Dependencies**: PDF, DOCX, EXCEL support bersifat optional. Sistem akan tetap berjalan tanpa mereka.
- **Warning Messages**: Jika library tidak terinstall, sistem akan menampilkan warning tapi tetap berjalan.
- **Performance**: PDF dengan OCR cukup berat. Untuk file besar, proses bisa memakan waktu.
- **Encoding**: Pastikan semua file dalam encoding UTF-8 untuk hasil terbaik.

---

**Version**: 2.1  
**Last Updated**: 2026-04-13  
**Status**: ✅ Complete Installation Guide
