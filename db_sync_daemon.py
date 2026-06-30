"""
Optional: Database Integration Script
Bisa dijalankan sebagai daemon untuk sync data dari database ke vectorstore

Script ini membaca tabel knowledge dari database dan 
otomatis menambahkannnya ke vectorstore
"""

import mysql.connector
from dotenv import load_dotenv
import requests
import json
import time
from datetime import datetime

load_dotenv()

BASE_URL = "http://localhost:8000"
POLL_INTERVAL = 10  # Check setiap 10 detik

class DatabaseSync:
    def __init__(self):
        self.processed_ids = set()
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "ai_chat"
        }
    
    def get_db(self):
        return mysql.connector.connect(**self.db_config)
    
    def sync_knowledge_from_db(self):
        """Baca knowledge baru dari database dan sync ke vectorstore"""
        try:
            conn = self.get_db()
            cursor = conn.cursor(dictionary=True)
            
            # Query untuk get knowledge yang belum di-process
            # Pastikan ada table 'knowledge' dengan columns: id, title, content, synced
            cursor.execute("""
                SELECT id, title, content 
                FROM knowledge 
                WHERE synced = 0 
                LIMIT 10
            """)
            
            results = cursor.fetchall()
            
            if not results:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ No new knowledge to sync")
                cursor.close()
                conn.close()
                return
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📚 Found {len(results)} new knowledge entries")
            
            for row in results:
                try:
                    knowledge_id = row['id']
                    
                    # Send ke API
                    payload = {
                        "title": row['title'],
                        "content": row['content']
                    }
                    
                    response = requests.post(
                        f"{BASE_URL}/add-knowledge",
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("status") == "success":
                            # Mark as synced
                            cursor.execute(
                                "UPDATE knowledge SET synced = 1, synced_at = NOW() WHERE id = %s",
                                (knowledge_id,)
                            )
                            conn.commit()
                            print(f"  ✅ ID {knowledge_id}: {row['title']}")
                        else:
                            print(f"  ⚠️ ID {knowledge_id}: API error - {result.get('message')}")
                    else:
                        print(f"  ❌ ID {knowledge_id}: HTTP {response.status_code}")
                
                except Exception as e:
                    print(f"  ❌ Error processing knowledge {knowledge_id}: {e}")
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Database Error: {e}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {e}")
    
    def start_daemon(self):
        """Run as daemon - continuously sync"""
        print("🔄 Database Sync Daemon Started")
        print(f"📌 Polling every {POLL_INTERVAL} seconds")
        print("⏹️  Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.sync_knowledge_from_db()
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\n\n🛑 Daemon stopped")


def create_knowledge_table():
    """Create knowledge table jika belum ada"""
    print("🔧 Setting up database...")
    
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ai_chat"
        )
        cursor = conn.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS knowledge (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            content LONGTEXT NOT NULL,
            synced TINYINT DEFAULT 0,
            synced_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_synced (synced),
            INDEX idx_created (created_at)
        );
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ Table 'knowledge' ready")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        # Setup mode - create table only
        create_knowledge_table()
    else:
        # Run daemon
        create_knowledge_table()
        sync = DatabaseSync()
        sync.start_daemon()
