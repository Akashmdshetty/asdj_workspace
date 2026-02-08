from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import ConnectionRequest

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'unique_id')
        read_only_fields = ('unique_id',)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ConnectionRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = ConnectionRequest
        fields = ('id', 'sender', 'receiver', 'status', 'created_at')
        read_only_fields = ('sender', 'receiver', 'status', 'created_at')

class SendRequestSerializer(serializers.Serializer):
    unique_id = serializers.CharField(max_length=6)

class RespondRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'reject'])

class TenantSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        from core.models import Tenant
        model = Tenant
        fields = ('id', 'name', 'slug', 'owner', 'created_at', 'is_owner')
        read_only_fields = ('id', 'slug', 'owner', 'created_at', 'is_owner')

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.owner == request.user
        return False

class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        from core.models import Membership
        model = Membership
        fields = ('id', 'user', 'role', 'joined_at')
        read_only_fields = ('id', 'user', 'joined_at')

class CreateTenantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
