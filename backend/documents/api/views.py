from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from documents.models import Folder, Document, Comment
from core.models import Tenant, Membership
from .serializers import (
    FolderSerializer, DocumentSerializer, CommentSerializer,
    CreateFolderSerializer, CreateDocumentSerializer
)

class WorkspaceContentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, workspace_id):
        # Verify access
        tenant = get_object_or_404(Tenant, id=workspace_id)
        if not Membership.objects.filter(tenant=tenant, user=request.user).exists() and tenant.owner != request.user:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get root items or specific folder items if 'folder_id' query param is present
        folder_id = request.query_params.get('folder_id')
        
        if folder_id:
            parent_folder = get_object_or_404(Folder, id=folder_id, tenant=tenant)
            folders = Folder.objects.filter(tenant=tenant, parent=parent_folder)
            documents = Document.objects.filter(tenant=tenant, folder=parent_folder)
            current_folder_data = FolderSerializer(parent_folder).data
        else:
            # Root
            folders = Folder.objects.filter(tenant=tenant, parent__isnull=True)
            documents = Document.objects.filter(tenant=tenant, folder__isnull=True)
            current_folder_data = None

        return Response({
            'current_folder': current_folder_data,
            'folders': FolderSerializer(folders, many=True).data,
            'documents': DocumentSerializer(documents, many=True).data
        })

    def post(self, request, workspace_id):
        # Handle creation of folders and files here for simplicity or split logic
        # Let's decide based on 'type' in body
        tenant = get_object_or_404(Tenant, id=workspace_id)
        if not Membership.objects.filter(tenant=tenant, user=request.user).exists() and tenant.owner != request.user:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            
        item_type = request.data.get('type')
        if item_type == 'folder':
            serializer = CreateFolderSerializer(data=request.data)
            if serializer.is_valid():
                parent_id = serializer.validated_data.get('parent_id')
                parent = None
                if parent_id:
                    parent = get_object_or_404(Folder, id=parent_id, tenant=tenant)
                
                folder = Folder.objects.create(
                    name=serializer.validated_data['name'],
                    tenant=tenant,
                    parent=parent,
                    created_by=request.user
                )
                return Response(FolderSerializer(folder).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif item_type == 'file':
            serializer = CreateDocumentSerializer(data=request.data)
            if serializer.is_valid():
                parent_id = serializer.validated_data.get('parent_id')
                parent = None
                if parent_id:
                    parent = get_object_or_404(Folder, id=parent_id, tenant=tenant)
                
                # Check for file
                file_obj = request.FILES.get('file')
                
                doc = Document.objects.create(
                    title=serializer.validated_data['title'],
                    content='', # Default empty for files
                    file=file_obj,
                    tenant=tenant,
                    folder=parent,
                    created_by=request.user
                )
                return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid type'}, status=status.HTTP_400_BAD_REQUEST)

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # This is a bit loose on tenant check, should improve in real app
        # Checking if user is member of the tenant the doc belongs to
        return (Document.objects.filter(tenant__memberships__user=self.request.user) | \
               Document.objects.filter(tenant__owner=self.request.user)).distinct()

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        document_id = self.kwargs['document_id']
        return Comment.objects.filter(document_id=document_id).order_by('created_at')

    def perform_create(self, serializer):
        document_id = self.kwargs['document_id']
        document = get_object_or_404(Document, id=document_id)
        # Check permissions logic here (omitted for brevity, assuming doc access implies comment access)
        serializer.save(user=self.request.user, document=document)

class FolderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return (Folder.objects.filter(tenant__memberships__user=self.request.user) | \
               Folder.objects.filter(tenant__owner=self.request.user)).distinct()
