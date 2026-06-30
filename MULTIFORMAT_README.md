# 🤖 Chatbot KMS Vector - Auto-Ingest v2.1

**Sistem otomatis untuk memproses SEMUA jenis dokumen (PDF, DOC, EXCEL, CSV, TXT)**

---

## 🎯 Fitur v2.1

✅ **Multi-Format Support** - TXT, PDF (OCR), DOC, EXCEL, CSV  
✅ **File Watcher** - Memantau folder `documents/` otomatis  
✅ **Upload Endpoint** - Upload file langsung ke API  
✅ **Add Knowledge Endpoint** - Tambah pengetahuan via API  
✅ **Background Thread** - Proses tanpa mengganggu chat  
✅ **Auto-Logging** - Catat setiap aksi di database  

---

## 📁 Format File yang Didukung

| Format | Ekstensi | Status | Fitur |
|--------|----------|--------|--------|
| Text | .txt | ✅ | Baca langsung |
| PDF | .pdf | ✅ | OCR + ekstrak teks |
| Word | .doc, .docx | ✅ | Ekstrak paragraf |
| Excel | .xlsx, .xls | ✅ | Baca semua sheet |
| CSV | .csv | ✅ | Parse sebagai tabel |

---

## 🚀 Quick Start (5 Menit)

### 1. Install Dependencies (Optional)
```bash
# Untuk support semua format
pip install python-docx openpyxl pytesseract pdf2image
```

### 2. Setup Database Table
```bash
python setup_db.py
```

### 3. Start API Server
```bash
uvicorn chat_api:app --reload
```

### 4. Verify Setup
```bash
python test_auto_ingest.py
```

**DONE!** 🎉 Sistem siap menerima semua jenis dokumen.

---

## 📝 3 Cara Menambah Pengetahuan

### Cara 1: Copy File ke Folder (Termudah)
```bash
# Copy SEMUA jenis file ke folder documents/
cp pengetahuan_baru.txt documents/
cp laporan.pdf documents/
cp data.xlsx documents/

# ✅ File akan otomatis diproses dalam 5 detik!
```

### Cara 2: Upload via API (Multi-Format)
```bash
# Upload PDF
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@documents/laporan.pdf"

# Upload Excel
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@documents/data.xlsx"

# Upload CSV
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@documents/data.csv"

# Upload Word
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@documents/dokumen.docx"
```

### Cara 3: Add Knowledge via API
```bash
curl -X POST "http://localhost:8000/add-knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Informasi Baru",
    "content": "Isi pengetahuan yang ingin ditambahkan..."
  }'
```

---

## 📊 Monitoring

### Check Vectorstore Status
```bash
curl http://localhost:8000/vectorstore-status
```

**Response:**
```json
{
  "status": "active",
  "documents": 500,
  "processed_files": 12,
  "message": "Vectorstore aktif dengan 500 dokumen"
}
```

### View All Endpoints & Supported Formats
```bash
curl http://localhost:8000/
```

---

## 📁 Struktur Folder

```
chatbot_kms_vector/
│
├── 📄 chat_api.py (MAIN - Multi-Format Support)
├── 🔧 setup_db.py (Setup database)
├── 🧪 test_auto_ingest.py (Test API)
├── 🔄 db_sync_daemon.py (Optional: DB sync)
│
├── 📂 documents/ (Input folder - ALL FORMATS)
│   ├── file1.txt ✅ Auto-processed
│   ├── laporan.pdf ✅ Auto-processed (OCR)
│   ├── data.xlsx ✅ Auto-processed
│   ├── info.docx ✅ Auto-processed
│   └── data.csv ✅ Auto-processed
│
└── 📂 vectorstore/ (Output)
    ├── index.faiss
    ├── index.pkl
    └── docstore.pkl
```

---

## 🔄 File Processing Flow

```
Dokumen Diupload/Ditambah (PDF/DOC/EXCEL/CSV/TXT)
         ↓
File Watcher Detects (every 5 sec)
         ↓
Auto Deteksi Format File
         ↓
Process Sesuai Format:
  - TXT: Baca langsung
  - PDF: OCR ekstrak teks
  - DOC: Ekstrak paragraf
  - EXCEL: Parse semua sheet
  - CSV: Convert ke teks
         ↓
Split into Chunks (700 chars, 150 overlap)
         ↓
Add to FAISS Vector DB
         ↓
Log to Document Log Table
         ↓
Ready for /chat queries ✅
```

---

## 💾 Fungsi Processing untuk Setiap Format

### Text File (.txt)
- Membaca file langsung
- Simple text extraction

### CSV File (.csv)
- Parse dengan csv.DictReader
- Convert setiap row menjadi text

### Word File (.docx, .doc)
- Ekstrak semua paragraf
- Requires: `python-docx`

### Excel File (.xlsx, .xls)
- Read semua sheets
- Convert cell content menjadi table format
- Requires: `openpyxl`

### PDF File (.pdf)
- Convert menjadi image
- OCR dengan pytesseract
- Requires: `pytesseract`, `pdf2image`

---

## ⚙️ Konfigurasi

### Ubah Interval File Watcher (di `chat_api.py`)
Cari line ~400:
```python
time.sleep(5)  # Ubah ke nilai lain (dalam detik)
```

### Ubah Chunk Size
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,        # Ukuran chunk (chars)
    chunk_overlap=150      # Overlap antar chunks
)
```

### Tesseract Path untuk PDF OCR
Edit di `process_pdf_file()` function:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### Poppler Path untuk PDF Conversion
```python
poppler_path = r"C:\\poppler\\poppler-25.12.0\\Library\\bin"
```

---

## 🆘 Troubleshooting

| Problem | Solusi |
|---------|--------|
| PDF tidak terbaca | Install: `pip install pytesseract pdf2image` |
| Excel error | Install: `pip install openpyxl` |
| DOC/DOCX error | Install: `pip install python-docx` |
| CSV encoding error | Pastikan file UTF-8 encoded |
| File tidak terdeteksi | Check console, pastikan format supported |
| Vectorstore kosong | Run: `curl -X POST http://localhost:8000/refresh-vectorstore` |
| Database error | Run: `python setup_db.py` untuk create tables |

---

## 🎓 Complete Example Workflow

```bash
# 1. Install dependencies
pip install python-docx openpyxl pytesseract pdf2image

# 2. Setup database
python setup_db.py

# 3. Start API server
uvicorn chat_api:app --reload

# 4. Add dokumen berbagai format
cp laporan.txt documents/
cp data.pdf documents/
cp sales.xlsx documents/
cp customers.csv documents/

# 5. Upload via endpoint (dengan delay untuk watcher)
sleep 5

# 6. Check status
curl http://localhost:8000/vectorstore-status

# 7. Chat dengan vectorstore
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Apa isi dari laporan?"}'

# 8. Monitor
curl http://localhost:8000/admin/chat-monitor
```

---

## 📊 Response Examples

### Upload PDF dengan OCR
```bash
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@laporan.pdf"
```

Console Output:
```
📤 File berhasil diupload: laporan.pdf (.pdf)
📄 Memproses laporan.pdf (.pdf)...
✅ 125 chunks ditambahkan ke vectorstore
```

Response:
```json
{
  "status": "success",
  "message": "125 dokumen berhasil diproses",
  "chunks": 125
}
```

### Upload Excel
```bash
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@data.xlsx"
```

Console Output:
```
📤 File berhasil diupload: data.xlsx (.xlsx)
📄 Memproses data.xlsx (.xlsx)...
✅ 45 chunks ditambahkan ke vectorstore
```

### Auto-Detect Format
File yang ditambahkan ke `documents/` otomatis dideteksi dan diproses:
```
📄 Memproses data.csv (.csv)...
📄 Memproses dokumen.docx (.docx)...
📄 Memproses tabel.xlsx (.xlsx)...
✅ Total 200 chunks ditambahkan ke vectorstore
```

---

## 🔍 API Endpoints Detail

### GET /
Info API dan supported formats

### POST /add-knowledge
Tambah pengetahuan text langsung
```json
{
  "title": "Judul dokumen",
  "content": "Isi konten..."
}
```

### POST /upload-document
Upload file (supporting semua format)
- Request: multipart/form-data dengan file
- Support: .txt, .pdf, .docx, .doc, .xlsx, .xls, .csv

### POST /chat
Chat query dengan vectorstore
```json
{
  "message": "Pertanyaan anda?"
}
```

### GET /vectorstore-status
Check status vectorstore

### POST /refresh-vectorstore
Manual refresh vectorstore

### GET /admin/chat-monitor
Monitor chat logs

---

## 🔮 Roadmap v2.2+

- [ ] Support image files (JPG, PNG) dengan Tesseract OCR
- [ ] DOCX advanced (tables, images, styles)
- [ ] PPTX (PowerPoint) support
- [ ] JSON/XML parsing
- [ ] Database direct integration (no folder needed)
- [ ] Webhook untuk automatic ingestion
- [ ] Advanced analytics dashboard
- [ ] Multi-model embeddings

---

**Last Updated:** 2026-04-13  
**Version:** 2.1  
**Status:** ✅ Production Ready - Multi-Format Support  
**Supported Formats:** TXT, PDF, DOC, EXCEL, CSV
