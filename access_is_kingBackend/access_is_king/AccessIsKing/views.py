from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user_auth.models import User
from AccessIsKing.models import (
City,
NewComments,
NewMessages,
)
 
from AccessIsKing.serializers import (
    CitySerializer,
   NewCommentSerializer,
   NewMessagesSerializer

)
from pyfcm import FCMNotification
from django.db.models import Q
import uuid


class CityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True, context={'request': request})
        return Response({'status': True, 'status_code': '200', 'message': '', "data": {"cities": serializer.data}}, status=200)

    def post(self, request):
        try:
            serializer = CitySerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'City created successfully!!!', 'data': {'city': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            city = get_object_or_404(City, pk=pk)
            serializer = CitySerializer(city, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'City updated successfully!!!', 'data': {'city': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            city = get_object_or_404(City, pk=pk)
            serializer = CitySerializer(city, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'City partially updated successfully!!!', 'data': {'city': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            city = get_object_or_404(City, pk=pk)
            city.delete()
            return Response({'status': True, 'status_code': '200', 'message': 'City deleted successfully!!!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cities =NewComments.objects.all()
        serializer =NewCommentSerializer(cities, many=True, context={'request': request})
        return Response({'status': True, 'status_code': '200', 'message': '', "data": {"cities": serializer.data}}, status=200)

    def post(self, request):
        try:
            serializer = NewCommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'City created successfully!!!', 'data': {'city': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            city = get_object_or_404(City, pk=pk)
            serializer = NewCommentSerializer(city, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'City updated successfully!!!', 'data': {'city': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            city = get_object_or_404(City, pk=pk)
            serializer = NewCommentSerializer(city, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'City partially updated successfully!!!', 'data': {'city': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            city = get_object_or_404(City, pk=pk)
            city.delete()
            return Response({'status': True, 'status_code': '200', 'message': 'City deleted successfully!!!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = NewMessages.objects.all()
        serializer = NewMessagesSerializer(messages, many=True, context={'request': request})
        return Response({'status': True, 'status_code': '200', 'message': '', "data": {"messages": serializer.data}}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = NewMessagesSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'Message created successfully!', 'data': {'message': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            message = get_object_or_404(NewMessages, pk=pk)
            serializer = NewMessagesSerializer(message, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'Message updated successfully!', 'data': {'message': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            message = get_object_or_404(NewMessages, pk=pk)
            serializer = NewMessagesSerializer(message, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'status_code': '200', 'message': 'Message partially updated successfully!', 'data': {'message': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, 'status_code': '400', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            message = get_object_or_404(NewMessages, pk=pk)
            message.delete()
            return Response({'status': True, 'status_code': '200', 'message': 'Message deleted successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, 'status_code': '500', "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)