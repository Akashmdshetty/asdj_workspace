from rest_framework import serializers
from backend.documents.models import Folder, Document, Comment
from backend.core.api.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

class FolderSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    # Recursion is tricky in DRF if we want full trees, but for typical file managers 
    # we just want to fetch one level at a time.
    
    class Meta:
        model = Folder
        fields = ('id', 'name', 'tenant', 'parent', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'tenant', 'created_by', 'created_at', 'updated_at')

class DocumentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Document
        fields = ('id', 'title', 'content', 'file', 'tenant', 'folder', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'tenant', 'created_by', 'created_at', 'updated_at')

class CreateFolderSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    parent_id = serializers.IntegerField(required=False, allow_null=True)

class CreateDocumentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    file = serializers.FileField(required=False, allow_null=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
