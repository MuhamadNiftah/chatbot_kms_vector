"""
Script untuk setup database tables yang diperlukan
Jalankan sekali saja di awal
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Connect ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ai_chat"
)

cursor = conn.cursor()

# Create table document_logs
create_table_sql = """
CREATE TABLE IF NOT EXISTS document_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    action VARCHAR(50),
    details JSON,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_action (action),
    INDEX idx_timestamp (timestamp)
);
"""

try:
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Table 'document_logs' berhasil dibuat/sudah ada")
except Exception as e:
    print(f"❌ Error: {e}")

# Verify table
cursor.execute("DESCRIBE document_logs;")
result = cursor.fetchall()
print("\n📋 Struktur Table:")
for row in result:
    print(f"  - {row[0]}: {row[1]}")

cursor.close()
conn.close()

print("\n✅ Setup database selesai!")
