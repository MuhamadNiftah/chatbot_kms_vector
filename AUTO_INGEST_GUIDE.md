# 📘 Panduan Auto-Ingest Sistem

## Fitur Baru (v2.0)

Sistem Chatbot KMS Vector sekarang sudah **OTOMATIS** memproses dokumen/pengetahuan yang masuk! 🚀

---

## 🎯 Cara Kerja

### 1. **File Watcher Otomatis** (Background Thread)
- Memantau folder `documents/` setiap 5 detik
- Otomatis membaca file `.txt` baru yang ditambahkan
- Otomatis memproses dan menambahkan ke vectorstore
- Tidak perlu jalankan `ingest.py` lagi!

### 2. **Upload Endpoint**
- **URL**: `POST /upload-document`
- **Cara**: Upload file `.txt` langsung ke API
- **Hasil**: File otomatis diproses dan masuk ke vectorstore

### 3. **Add Knowledge Endpoint** 
- **URL**: `POST /add-knowledge`
- **Cara**: Kirim teks/pengetahuan langsung via API
- **Format**: JSON dengan field `title` dan `content`
- **Hasil**: Langsung ditambahkan ke vectorstore

---

## 📋 Cara Menggunakan

### Metode 1: Upload File (Rekomendasi)
```bash
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@documents/pengetahuan_baru.txt"
```

**Response:**
```json
{
  "status": "success",
  "message": "48 dokumen berhasil diproses",
  "chunks": 48
}
```

---

### Metode 2: Add Knowledge Teks (API)
```bash
curl -X POST "http://localhost:8000/add-knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pengetahuan Baru",
    "content": "Ini adalah pengetahuan baru yang ingin ditambahkan ke sistem..."
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "1 dokumen berhasil diproses",
  "chunks": 1
}
```

---

### Metode 3: Copy File ke Folder (Otomatis)
Cukup copy/paste file `.txt` ke folder `documents/`
- File watcher akan otomatis mendeteksi dalam 5 detik
- Otomatis diproses tanpa perlu aksi tambahan
- Bisa bersamaan dengan file lain

---

## 📊 Cek Status

### Check Vectorstore Status
```bash
curl "http://localhost:8000/vectorstore-status"
```

**Response:**
```json
{
  "status": "active",
  "documents": 156,
  "processed_files": 5,
  "message": "Vectorstore aktif dengan 156 dokumen"
}
```

---

### Monitor Chat Logs
```bash
curl "http://localhost:8000/admin/chat-monitor"
```

---

## 🗂️ Struktur Folder

```
chatbot_kms_vector/
├── chat_api.py (SUDAH DIUPDATE)
├── ingest.py (LEGACY - tidak perlu lagi)
├── documents/
│   ├── file1.txt ✅ Auto-processed
│   ├── file2.txt ✅ Auto-processed
│   └── file_baru.txt ✅ Auto-processed
├── vectorstore/
│   ├── index.faiss
│   ├── index.pkl
│   └── docstore.pkl
```

---

## 🔧 Konfigurasi

### Interval File Watcher
Edit di `chat_api.py` line ~130:
```python
time.sleep(5)  # Ubah ke nilai lain (dalam detik)
```

### Chunk Size untuk Text Splitter
Edit di `chat_api.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,        # Ukuran potongan
    chunk_overlap=150      # Overlap antar potongan
)
```

---

## 💾 Database Logging

Sistem mencatat setiap aksi di tabel `document_logs`:

```sql
CREATE TABLE IF NOT EXISTS document_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    action VARCHAR(50),
    details JSON,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Jenis Action:**
- `auto_ingest` - File watcher otomatis
- `upload_file` - Upload via endpoint
- `manual_add` - Add knowledge via endpoint

---

## ⚙️ Setup Awal

1. **Jalankan API:**
```bash
uvicorn chat_api:app --reload
```

2. **Upload dokumen pertama:**
   - Upload via endpoint, atau
   - Copy file ke folder `documents/`

3. **Tunggu 5 detik** - File watcher akan otomatis memproses

4. **Start chatting!** 🎉

---

## 🆘 Troubleshooting

### Vectorstore Kosong?
```bash
# Check status
curl "http://localhost:8000/vectorstore-status"

# Refresh manual
curl -X POST "http://localhost:8000/refresh-vectorstore"
```

### File Tidak Terdeteksi?
- Pastikan format `.txt` (case-sensitive)
- Check console untuk error message
- Pastikan encoding UTF-8

### Database Error?
- Pastikan tabel `document_logs` sudah dibuat
- Check koneksi MySQL

---

## 📈 Roadmap v3.0

- [ ] Support file PDF dengan OCR
- [ ] Webhook untuk auto-ingest dari source lain
- [ ] API Analytics dashboard
- [ ] Multi-vectorstore support

---

**Last Updated:** 2026-04-13  
**Version:** 2.0 - Auto-Ingest
