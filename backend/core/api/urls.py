from django.urls import path
from .views import (
    RegisterView, LoginView, UserProfileView,
    SendConnectionRequestView, ConnectionRequestsView, RespondConnectionRequestView,
    TenantListCreateView, TenantDetailView, TenantMembershipView
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/me/', UserProfileView.as_view(), name='profile'),
    path('connections/send/', SendConnectionRequestView.as_view(), name='send-request'),
    path('connections/pending/', ConnectionRequestsView.as_view(), name='pending-requests'),
    path('connections/<int:pk>/respond/', RespondConnectionRequestView.as_view(), name='respond-request'),
    
    # Workspaces
    path('workspaces/', TenantListCreateView.as_view(), name='workspace-list'),
    path('workspaces/<int:id>/', TenantDetailView.as_view(), name='workspace-detail'),
    path('workspaces/<int:tenant_id>/members/', TenantMembershipView.as_view(), name='workspace-members'),
]
