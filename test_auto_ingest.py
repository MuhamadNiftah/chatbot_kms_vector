"""
Script Test untuk demonstrasi Auto-Ingest API
Jalankan setelah server chat_api.py sudah running
"""

import requests
import json
from pathlib import Path

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


def test_api_info():
    """Test endpoint root"""
    print("\n🔍 TEST 1: Get API Info")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "API Info")


def test_vectorstore_status():
    """Test check vectorstore status"""
    print("\n🔍 TEST 2: Check Vectorstore Status")
    response = requests.get(f"{BASE_URL}/vectorstore-status")
    print_response(response, "Vectorstore Status")


def test_add_knowledge():
    """Test add knowledge endpoint"""
    print("\n🔍 TEST 3: Add Knowledge (Text)")
    
    payload = {
        "title": "Pengetahuan Test",
        "content": """
        Ini adalah contoh pengetahuan yang ditambahkan secara otomatis.
        Sistem ini dapat memproses informasi baru dengan mudah.
        Setiap pengetahuan akan di-embedding dan disimpan di vectorstore.
        """
    }
    
    response = requests.post(
        f"{BASE_URL}/add-knowledge",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "Add Knowledge Result")


def test_upload_file():
    """Test upload file endpoint"""
    print("\n🔍 TEST 4: Upload Document File")
    
    # Create test file
    test_file_path = "documents/test_knowledge.txt"
    Path("documents").mkdir(exist_ok=True)
    
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write("""
        INFORMASI TEKNOLOGI
        
        Artificial Intelligence (AI) adalah teknologi yang memungkinkan komputer
        untuk belajar dan membuat keputusan berdasarkan data.
        
        Machine Learning adalah subset dari AI yang fokus pada pembelajaran
        dari data tanpa pemrograman eksplisit.
        
        Deep Learning menggunakan neural networks untuk memproses data kompleks.
        """)
    
    with open(test_file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{BASE_URL}/upload-document",
            files=files
        )
    print_response(response, "Upload File Result")


def test_refresh_vectorstore():
    """Test refresh vectorstore"""
    print("\n🔍 TEST 5: Refresh Vectorstore")
    response = requests.post(f"{BASE_URL}/refresh-vectorstore")
    print_response(response, "Refresh Result")


def test_chat():
    """Test chat endpoint"""
    print("\n🔍 TEST 6: Chat Query")
    
    payload = {
        "message": "Apa itu AI dan Machine Learning?"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "Chat Response")


def test_admin_monitor():
    """Test admin monitoring"""
    print("\n🔍 TEST 7: Admin Chat Monitor")
    response = requests.get(f"{BASE_URL}/admin/chat-monitor")
    print_response(response, "Chat Logs (Last 10)")


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("🚀" * 30)
    print("AUTO-INGEST API TEST SUITE")
    print("🚀" * 30)
    
    try:
        test_api_info()
        
        input("\n✋ Press ENTER to continue to next test...")
        test_vectorstore_status()
        
        input("\n✋ Press ENTER to continue to next test...")
        test_add_knowledge()
        
        input("\n✋ Press ENTER to continue to next test...")
        test_upload_file()
        
        input("\n✋ Press ENTER to continue to next test (tunggu file watcher memproses)...")
        test_vectorstore_status()
        
        input("\n✋ Press ENTER to continue to next test...")
        test_chat()
        
        input("\n✋ Press ENTER to view monitoring...")
        test_admin_monitor()
        
        print("\n" + "✅" * 30)
        print("SEMUA TEST SELESAI!")
        print("✅" * 30)
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Tidak bisa connect ke server!")
        print("📌 Pastikan API sudah running: uvicorn chat_api:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    run_all_tests()
