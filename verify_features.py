import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.local')
django.setup()
from backend.documents.models import Document, Comment, Folder
from backend.core.models import User, Tenant

def verify_features():
    print("Verifying Backend Features...")
    
    user = User.objects.first()
    tenant = Tenant.objects.first()
    
    # 1. Test File Upload
    print("\n--- Testing File Upload ---")
    file_content = b"This is a test file content."
    uploaded_file = SimpleUploadedFile("test_upload.txt", file_content, content_type="text/plain")
    
    doc = Document.objects.create(
        title="Uploaded Doc",
        file=uploaded_file,
        tenant=tenant,
        created_by=user
    )
    
    if doc.file:
        print(f"PASS: File uploaded path: {doc.file.name}")
        # Verify content retrieval if needed, but existence is key
    else:
        print("FAIL: File not uploaded.")

    # 2. Test Comments
    print("\n--- Testing Comments ---")
    comment = Comment.objects.create(
        document=doc,
        user=user,
        text="This is a test comment."
    )
    
    saved_comment = Comment.objects.filter(document=doc).first()
    if saved_comment and saved_comment.text == "This is a test comment.":
        print(f"PASS: Comment created successfully: '{saved_comment.text}'")
    else:
        print("FAIL: Comment creation failed.")

if __name__ == "__main__":
    verify_features()
