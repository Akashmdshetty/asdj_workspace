import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.local')
django.setup()
from backend.documents.models import Folder, Document

def verify():
    print("Verifying Agent Work...")
    
    # Check Folder
    folder = Folder.objects.filter(name='Agent Docs').first()
    if folder:
        print(f"PASS: Found folder 'Agent Docs' (ID: {folder.id})")
    else:
        print("FAIL: Folder 'Agent Docs' not found.")
        return

    # Check File
    doc = Document.objects.filter(title='Test File', folder=folder).first()
    if doc:
        print(f"PASS: Found file 'Test File' inside 'Agent Docs' (ID: {doc.id})")
    else:
        print("FAIL: File 'Test File' not found inside folder.")

if __name__ == "__main__":
    verify()
