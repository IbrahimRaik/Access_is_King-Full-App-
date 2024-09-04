from rest_framework import serializers
from user_auth.models import Token, User, BIDNumber
import logging
import uuid
from django.contrib.auth.password_validation import validate_password

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=200, default="", read_only=True)
    name = serializers.CharField(max_length=200, default="")
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=20, required=False)
    avatar = serializers.CharField(max_length=200, default="", required=False)
    remember_token = serializers.CharField(max_length=200, default="", required=False)
    login_mode = serializers.CharField(max_length=200, default='Email')
    status = serializers.CharField(max_length=200, default='Active')
    is_active = serializers.BooleanField(default=True)
    auth_provider = serializers.CharField(max_length=255, default="Email")
    auth_token = serializers.CharField(max_length=255, default="Email")
    bid = serializers.CharField(source='bid.bid', read_only=True)  # Add BID field

    class Meta:
        model = User
        fields = ['id', 'code', 'email', 'name', 'password', 'phone', 'avatar', 'remember_token', 'login_mode', 'status', 'is_active', 'auth_provider', 'auth_token', 'bid']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def validate(self, attrs):
        return attrs

class UserRegistrationSerializer(serializers.ModelSerializer):
    bid = serializers.CharField(write_only=True)  # Expect BID to be passed

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'phone', 'auth_provider', 'auth_token', 'bid']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_bid(self, value):
        # Check if the BID number exists and is unused
        try:
            bid = BIDNumber.objects.get(bid=value, is_used=False)
        except BIDNumber.DoesNotExist:
            raise serializers.ValidationError("Invalid or already used BID number")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        # Fetch the valid BID number
        bid_number = validated_data.pop('bid')
        bid = BIDNumber.objects.get(bid=bid_number, is_used=False)
        
        # Create the user and associate the BID number
        user_instance = User.objects.create_user(**validated_data, bid=bid)
        
        # Mark the BID as used
        bid.is_used = True
        bid.save()

        return user_instance

class UserLoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

class UserInformationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=0, read_only=True)
    email = serializers.CharField(default="", read_only=True)
    name = serializers.CharField(default="", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def save(self):
        user = self.context['request'].user
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()
        return user

class SocialLoginSerializers(serializers.ModelSerializer):
    auth_token = serializers.CharField(max_length=255)
    auth_provider = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['auth_token', 'auth_provider']

class TokensSerializer(serializers.ModelSerializer):
    key = serializers.CharField(max_length=4048)
    user = serializers.IntegerField(default=0)

    class Meta:
        model = Token
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']
