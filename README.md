# 🤖 Chatbot KMS Vector - Auto-Ingest v2.0

**Sistem otomatis untuk memproses pengetahuan/dokumen yang masuk secara real-time**

---

## 🎯 Fitur Baru

✅ **File Watcher** - Memantau folder `documents/` otomatis  
✅ **Upload Endpoint** - Upload file langsung ke API  
✅ **Add Knowledge Endpoint** - Tambah pengetahuan via API  
✅ **Background Thread** - Proses tanpa mengganggu chat  
✅ **Auto-Logging** - Catat setiap aksi di database  

---

## 🚀 Quick Start (5 Menit)

### 1. Setup Database Table
```bash
python setup_db.py
```

### 2. Start API Server
```bash
uvicorn chat_api:app --reload
```

### 3. Verify Setup
```bash
python test_auto_ingest.py
```

**DONE!** 🎉 Sistem siap menerima dokumen otomatis.

---

## 📝 3 Cara Menambah Pengetahuan

### Cara 1: Copy File ke Folder (Termudah)
```bash
# Copy file .txt ke folder documents/
cp pengetahuan_baru.txt documents/

# ✅ File akan otomatis diproses dalam 5 detik!
```

### Cara 2: Upload via API
```bash
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@documents/pengetahuan.txt"
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
  "documents": 150,
  "processed_files": 5
}
```

### View All Endpoints
```bash
curl http://localhost:8000/
```

---

## 📁 Struktur Folder

```
chatbot_kms_vector/
│
├── 📄 chat_api.py (MAIN - Auto-Ingest)
├── 🔧 setup_db.py (Setup database)
├── 🧪 test_auto_ingest.py (Test API)
├── 🔄 db_sync_daemon.py (Optional: DB sync)
│
├── 📂 documents/ (Input folder)
│   ├── file1.txt ✅ Auto-processed
│   ├── file2.txt ✅ Auto-processed
│   └── file3.txt ✅ Auto-processed
│
└── 📂 vectorstore/ (Output)
    ├── index.faiss
    ├── index.pkl
    └── docstore.pkl
```

---

## 🔄 How It Works

```
Document Uploaded/Added
         ↓
File Watcher Detects (every 5 sec)
         ↓
Process & Split into Chunks
         ↓
Add to FAISS Vector DB
         ↓
Log to Database
         ↓
Ready for /chat endpoint
```

---

## ⚙️ Konfigurasi

### Ubah Interval Check (di `chat_api.py`)
```python
time.sleep(5)  # Ubah ke nilai lain misalnya 10
```

### Ubah Chunk Size
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,        # Ubah ukuran
    chunk_overlap=150      # Ubah overlap
)
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Vectorstore Kosong | Run `curl -X POST http://localhost:8000/refresh-vectorstore` |
| File Tidak Terdeteksi | Pastikan format `.txt`, check console untuk error |
| Database Error | Run `setup_db.py` untuk create tables |
| API Error | Check `.env` file untuk API keys |

---

## 📚 Dokumentasi Lengkap

Baca file `AUTO_INGEST_GUIDE.md` untuk dokumentasi detail.

---

## 🎓 Example Workflow

```bash
# 1. Setup
python setup_db.py
uvicorn chat_api:app --reload
python test_auto_ingest.py

# 2. Add Knowledge
curl -X POST "http://localhost:8000/add-knowledge" \
  -H "Content-Type: application/json" \
  -d '{"title": "AI Basics", "content": "AI adalah..."}'

# 3. Check Status
curl http://localhost:8000/vectorstore-status

# 4. Chat
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Apa itu AI?"}'
```

---

## 🔮 Future Roadmap

- [ ] Support PDF files dengan OCR
- [ ] Webhook untuk external sources
- [ ] Analytics dashboard
- [ ] Multi-embedding models
- [ ] Real-time streaming responses

---

**Last Updated:** 2026-04-13  
**Version:** 2.0  
**Status:** ✅ Production Ready
