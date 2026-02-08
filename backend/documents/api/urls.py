from django.urls import path
from .views import WorkspaceContentListView, DocumentDetailView, CommentListCreateView, FolderDetailView

urlpatterns = [
    path('workspaces/<int:workspace_id>/content/', WorkspaceContentListView.as_view(), name='workspace-content'),
    path('documents/<int:id>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:document_id>/comments/', CommentListCreateView.as_view(), name='document-comments'),
    path('folders/<int:id>/', FolderDetailView.as_view(), name='folder-detail'),
]
