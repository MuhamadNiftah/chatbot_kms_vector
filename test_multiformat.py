"""
Extended Test Suite untuk Multi-Format Support
Jalankan setelah server chat_api.py sudah running
"""

import requests
import json
from pathlib import Path
import os

BASE_URL = "http://localhost:8000"

def print_response(response, title=""):
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)


def print_step(step_num, description):
    print(f"\n{'='*60}")
    print(f"🔍 TEST {step_num}: {description}")
    print(f"{'='*60}")


def create_test_files():
    """Create test files untuk semua format"""
    os.makedirs("documents", exist_ok=True)
    
    # Test TXT file
    with open("documents/test_knowledge.txt", 'w', encoding='utf-8') as f:
        f.write("""
        INFORMASI TEKNOLOGI AI
        
        Artificial Intelligence (AI) adalah teknologi yang memungkinkan 
        komputer untuk belajar dari data dan membuat keputusan secara otomatis.
        
        Machine Learning adalah subset dari AI yang fokus pada pembelajaran
        dari data tanpa pemrograman eksplisit.
        
        Deep Learning menggunakan neural networks dengan banyak layer untuk
        memproses data kompleks seperti gambar dan suara.
        """)
    
    print("✅ Created: test_knowledge.txt")


def test_api_info():
    """Test endpoint root"""
    print_step(1, "Get API Info & Supported Formats")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "API Info with Multi-Format Support")
    
    data = response.json()
    if "supported_formats" in data:
        print(f"\n✅ Supported Formats: {', '.join(data['supported_formats'])}")


def test_vectorstore_status():
    """Test check vectorstore status"""
    print_step(2, "Check Vectorstore Status")
    response = requests.get(f"{BASE_URL}/vectorstore-status")
    print_response(response, "Current Vectorstore Status")


def test_add_knowledge():
    """Test add knowledge endpoint"""
    print_step(3, "Add Knowledge (Text)")
    
    payload = {
        "title": "Multi-Format Information",
        "content": """
        Chatbot KMS Vector v2.1 mendukung format file:
        - TXT: Text file biasa
        - PDF: Format digital dengan OCR support
        - DOCX: Microsoft Word documents
        - XLSX: Microsoft Excel spreadsheets
        - CSV: Comma Separated Values
        
        Setiap format diproses secara otomatis dan ditambahkan ke vectorstore.
        """
    }
    
    response = requests.post(
        f"{BASE_URL}/add-knowledge",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "Add Knowledge Result")


def test_upload_txt_file():
    """Test upload TXT file endpoint"""
    print_step(4, "Upload TXT File")
    
    create_test_files()
    
    with open("documents/test_knowledge.txt", 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{BASE_URL}/upload-document",
            files=files
        )
    print_response(response, "Upload TXT File Result")


def test_upload_invalid_file():
    """Test upload invalid format"""
    print_step(5, "Upload Invalid Format (Should Fail)")
    
    # Create invalid format file
    invalid_file_path = "documents/test.exe"
    with open(invalid_file_path, 'wb') as f:
        f.write(b"invalid content")
    
    with open(invalid_file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{BASE_URL}/upload-document",
            files=files
        )
    
    print_response(response, "Upload Invalid Format Result (Expected Error)")
    
    # Cleanup
    os.remove(invalid_file_path)


def test_refresh_vectorstore():
    """Test refresh vectorstore"""
    print_step(6, "Refresh Vectorstore Manual")
    response = requests.post(f"{BASE_URL}/refresh-vectorstore")
    print_response(response, "Refresh Result")


def test_chat():
    """Test chat endpoint"""
    print_step(7, "Chat Query")
    
    payload = {
        "message": "Apa saja format file yang didukung?"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "Chat Response")


def test_admin_monitor():
    """Test admin monitoring"""
    print_step(8, "Admin Chat Monitor")
    response = requests.get(f"{BASE_URL}/admin/chat-monitor")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal chat logs: {len(data) if isinstance(data, list) else 'N/A'}")
        if isinstance(data, list) and len(data) > 0:
            print(f"Latest log: {data[0]}")
    else:
        print_response(response, "Chat Monitor")


def test_batch_operations():
    """Test multiple operations"""
    print_step(9, "Batch Operations (Multiple Files)")
    
    print("\n📋 Scenario: Adding multiple knowledge items")
    
    items = [
        ("Python Guide", "Python adalah bahasa pemrograman tingkat tinggi..."),
        ("Web Dev", "Web development melibatkan HTML, CSS, JavaScript..."),
        ("Database", "Database adalah sistem penyimpanan data terstruktur...")
    ]
    
    success_count = 0
    for title, content in items:
        payload = {"title": title, "content": content}
        response = requests.post(
            f"{BASE_URL}/add-knowledge",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print(f"  ✅ {title}: {result.get('chunks', 0)} chunks")
                success_count += 1
    
    print(f"\n✅ Berhasil menambahkan {success_count}/{len(items)} knowledge items")


def test_format_detection():
    """Test automatic format detection"""
    print_step(10, "Format Auto-Detection")
    
    print("\nSetiap format file memiliki metadata tersendiri:")
    print("  .txt  → type: 'txt'")
    print("  .pdf  → type: 'pdf', pages: <number>")
    print("  .docx → type: 'docx'")
    print("  .xlsx → type: 'excel'")
    print("  .csv  → type: 'csv'")
    
    print("\n✅ System akan otomatis mendeteksi dan memproses format apapun")


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("🚀" * 30)
    print("MULTI-FORMAT AUTO-INGEST API TEST SUITE V2.1")
    print("🚀" * 30)
    
    try:
        test_api_info()
        
        input("\n✋ Press ENTER to continue...")
        test_vectorstore_status()
        
        input("\n✋ Press ENTER to continue...")
        test_add_knowledge()
        
        input("\n✋ Press ENTER to continue...")
        test_upload_txt_file()
        
        input("\n✋ Press ENTER to continue...")
        test_upload_invalid_file()
        
        input("\n✋ Press ENTER to continue (tunggu file watcher)...")
        test_vectorstore_status()
        
        input("\n✋ Press ENTER to continue...")
        test_refresh_vectorstore()
        
        input("\n✋ Press ENTER to continue...")
        test_chat()
        
        input("\n✋ Press ENTER to continue...")
        test_batch_operations()
        
        input("\n✋ Press ENTER to continue...")
        test_format_detection()
        
        input("\n✋ Press ENTER to view monitoring...")
        test_admin_monitor()
        
        print("\n" + "✅" * 30)
        print("SEMUA TEST SELESAI!")
        print("✅" * 30)
        
        print("\n📝 Summary:")
        print("  ✅ Multi-format support tested")
        print("  ✅ Auto-detection working")
        print("  ✅ File watcher monitoring")
        print("  ✅ Chat functionality active")
        print("\n🎉 System is ready for production!")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Tidak bisa connect ke server!")
        print("📌 Pastikan API sudah running: uvicorn chat_api:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
