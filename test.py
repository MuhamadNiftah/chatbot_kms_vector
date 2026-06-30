import sys
sys.path.append("c:\\xampp\\htdocs\\chatbot_kms_vector")
import chat_api
doc = chat_api.process_pdf_file("c:\\xampp\\htdocs\\chatbot_kms_vector\\documents\\1777284961_COMPROF DIDIMAX 2025 HD.pdf")
print("Extracted content length:", len(doc.page_content) if doc else "None")
print("Preview:", doc.page_content[:500] if doc else "")
