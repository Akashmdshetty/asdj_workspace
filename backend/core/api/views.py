from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models # Added models import for Q objects
from core.models import ConnectionRequest, ConnectionRequest, Tenant, Membership
from .serializers import (
    UserSerializer, LoginSerializer, ConnectionRequestSerializer,
    SendRequestSerializer, RespondRequestSerializer,
    TenantSerializer, MembershipSerializer, CreateTenantSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Basic registration that handles password setting
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        if email and User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
            
        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class SendConnectionRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = SendRequestSerializer(data=request.data)
        if serializer.is_valid():
            target_id = serializer.validated_data['unique_id']
            try:
                receiver = User.objects.get(unique_id=target_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                
            if receiver == request.user:
                return Response({'error': 'Cannot add yourself'}, status=status.HTTP_400_BAD_REQUEST)
                
            if ConnectionRequest.objects.filter(sender=request.user, receiver=receiver).exists():
                return Response({'error': 'Request already sent'}, status=status.HTTP_400_BAD_REQUEST)

            conn_req = ConnectionRequest.objects.create(sender=request.user, receiver=receiver)
            return Response(ConnectionRequestSerializer(conn_req).data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConnectionRequestsView(generics.ListAPIView):
    serializer_class = ConnectionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Incoming pending requests
        return ConnectionRequest.objects.filter(receiver=self.request.user, status='pending')

class RespondConnectionRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        conn_req = get_object_or_404(ConnectionRequest, pk=pk, receiver=request.user, status='pending')
        serializer = RespondRequestSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data['action']
            if action == 'accept':
                conn_req.status = 'accepted'
                conn_req.save()
                # logic to create friendship/membership could go here
            elif action == 'reject':
                conn_req.status = 'rejected'
                conn_req.save()
            return Response({'status': conn_req.status})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TenantListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTenantSerializer
        return TenantSerializer

    def get_queryset(self):
        # Return tenants where user is a member
        return Tenant.objects.filter(memberships__user=self.request.user)

    def perform_create(self, serializer):
        from django.utils.text import slugify
        import uuid
        
        name = serializer.validated_data['name']
        slug = slugify(name) + '-' + str(uuid.uuid4())[:8]
        tenant = Tenant.objects.create(name=name, slug=slug, owner=self.request.user)
        
        # Add owner as admin member
        Membership.objects.create(user=self.request.user, tenant=tenant, role='admin')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'status': 'Workspace created'}, status=status.HTTP_201_CREATED)

class TenantDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TenantSerializer
    lookup_field = 'id'

    def get_queryset(self):
         return Tenant.objects.filter(memberships__user=self.request.user)

class TenantMembershipView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, tenant_id):
        # List members of a tenant
        tenant = get_object_or_404(Tenant, id=tenant_id, memberships__user=request.user)
        members = Membership.objects.filter(tenant=tenant)
        return Response(MembershipSerializer(members, many=True).data)

    def post(self, request, tenant_id):
        # Add member (only if requester is admin/owner ideally, simplifying for now)
        tenant = get_object_or_404(Tenant, id=tenant_id, memberships__user=request.user)
        
        # Check if requester is admin/owner
        if not Membership.objects.filter(tenant=tenant, user=request.user, role='admin').exists() and tenant.owner != request.user:
             return Response({'error': 'Only admins can add members'}, status=status.HTTP_403_FORBIDDEN)

        target_unique_id = request.data.get('unique_id')
        try:
            user_to_add = User.objects.get(unique_id=target_unique_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if they are connected
        # Either A->B or B->A with status='accepted'
        is_connected = ConnectionRequest.objects.filter(
            (models.Q(sender=request.user, receiver=user_to_add) | models.Q(sender=user_to_add, receiver=request.user)),
            status='accepted'
        ).exists()
        
        # Also allow if adding self (conceptually ok, but already added on create)
        if user_to_add != request.user and not is_connected:
             return Response({'error': 'User is not in your connections'}, status=status.HTTP_400_BAD_REQUEST)

        if Membership.objects.filter(tenant=tenant, user=user_to_add).exists():
             return Response({'error': 'User is already a member'}, status=status.HTTP_400_BAD_REQUEST)

        Membership.objects.create(tenant=tenant, user=user_to_add, role='member')
        return Response({'status': 'Member added'}, status=status.HTTP_201_CREATED)
