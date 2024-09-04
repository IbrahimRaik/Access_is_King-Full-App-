from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from user_auth.models import Token, User
from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
import uuid
from pyfcm import FCMNotification
import traceback
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from user_auth.serializers import PasswordResetSerializer, TokensSerializer, UserLoginSerializers, UserRegistrationSerializer
from .models import BIDNumber
import random
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }



class GenerateBIDNumberView(APIView):
    def get(self, request, format=None):
        bid_number = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit number
        
        while BIDNumber.objects.filter(bid=bid_number).exists():
            bid_number = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Ensure it's unique

        bid = BIDNumber.objects.create(bid=bid_number)
        
        return Response({
            'status': True,
            'bid_number': bid.bid
        }, status=status.HTTP_200_OK)
    def post(self, request, format=None):
        bid_number = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit number
        
        while BIDNumber.objects.filter(bid=bid_number).exists():
            bid_number = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Ensure it's unique

        bid = BIDNumber.objects.create(bid=bid_number, is_used=False)  # Ensure it's not used yet
        
        return Response({
            'status': True,
            'bid_number': bid.bid
        }, status=status.HTTP_200_OK)

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        bid_number = request.data.get('bid')
        
        # Check if the BID is valid and unused
        try:
            bid = BIDNumber.objects.get(bid=bid_number, is_used=False)
        except BIDNumber.DoesNotExist:
            return Response({
                'status': False, 
                'message': 'Invalid or already used BID number',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(bid=bid)  # Associate user with the valid BID number
            bid.is_used = True  # Mark the BID as used
            bid.save()

            token_key = get_tokens_for_user(user)['access']
            return Response({
                'status': True, 
                'status_code': 200, 
                'message': 'Registration Successful', 
                'data': {
                    'user': serializer.data,
                    'token': token_key,
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': False, 
            'status_code': 400, 
            'message': 'Email already exists',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:
                key = get_tokens_for_user(user)

                token_data = {
                    "key": key["access"],
                    "user": user.id
                }

                token_serializer = TokensSerializer(data=token_data)
                if token_serializer.is_valid():
                    token_serializer.save()

                profile_serializer = UserRegistrationSerializer(user)

                return Response({
                    'status': True,
                    'status_code': 200,
                    'message': 'SignIn Success',
                    'data': {
                        'user': {
                            'name': user.name,
                            'email': user.email,
                            'phone': user.phone,
                        },
                        
                        'profile': profile_serializer.data,
                        'token': key
                    }
                }, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({
                    'status': False,
                    'status_code': 400,
                    'message': 'Invalid Credentials, Please try again',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': False,
                'status_code': 400,
                'message': 'Invalid data',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)