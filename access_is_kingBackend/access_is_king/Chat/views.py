from django.shortcuts import render
from Chat.models import Conversation , Message
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from user_auth.models import  User 
from user_auth.serializers import UserProfileSerializer 
from Chat.models import Conversation, Message, Group, GroupMessage, Event, EventParticipant
from Chat.serializers import (
    ConversationIDSerializer, ConversationListSerializer, MessageSerializer,
    GroupSerializer, GroupMessageSerializer, EventSerializer, EventParticipantSerializer
)

from django.db.models import Q
from django.shortcuts import redirect, reverse
from rest_framework.permissions import IsAuthenticated
from pyfcm import FCMNotification
import datetime

# Create your views here.
@api_view(['POST'])
def start_convo(request):
    data = request.data
    username = data.pop('username')
    try:
        participant = User.objects.get(email=username)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non-existent user'}, status=status.HTTP_404_NOT_FOUND)

    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))
    if conversation.exists():
        conversation = conversation.first()
    else:
        conversation = Conversation.objects.create(initiator=request.user, receiver=participant)

    serializer = ConversationIDSerializer(instance=conversation)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id, sender=request.user)
    except Message.DoesNotExist:
        return Response({'message': 'Message not found or you do not have permission to delete this message.'}, 
                        status=status.HTTP_404_NOT_FOUND)

    message.delete()
    return Response({'message': 'Message deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'})
    # else:
    #     serializer = ConversationSerializer(instance=conversation[0])
    #     return Response(serializer.data)
    else:
        serializer = ConversationIDSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def postMessage(request):
    permission_classes = [IsAuthenticated]    
    conv_id=request.data['conversation_id']
    serializer =  MessageSerializer(data=request.data)
    if serializer.is_valid():
        #Getting USer
        ruser = UserProfileSerializer(request.user) 
        user_id=ruser.data["id"]
        user=User.objects.get(id=user_id)
        
        #Getting Conversation
        conv=Conversation.objects.get(id=conv_id)
        print('This sis the convo id :- ', conv)

        serializer.validated_data["sender"]= user
        serializer.validated_data["conversation_id"]= conv        
        msg=serializer.save()
        print('This sis the convo id :- ', conv.initiator.id)

        time = str(datetime.datetime.now())
        print(type(time))
        if serializer.is_valid():
            message_data = {
                'sender':conv.initiator.id,
                'text':request.data['text'],
                'conversation_id':request.data['conversation_id'],
                'timestamp': time
            }
            print(message_data)
            return Response({'status':'SUCCESS', 'status_code':'200' , 'message':'Message send  Successfully', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
    return Response({'status':'Error', 'status_code':'400' , 'message':'Invalid Credentials Please try again', 'data':None }, status=status.HTTP_202_ACCEPTED)  


@api_view(['POST'])
def create_group(request):
    data = request.data
    admin = request.user
    group = Group.objects.create(name=data['name'], admin=admin)
    group.participants.add(admin)
    serializer = GroupSerializer(instance=group)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_groups(request):
    # Get all groups
    groups = Group.objects.all()
    
    # Serialize the groups
    serializer = GroupSerializer(groups, many=True)
    
    # Return the serialized data
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# def add_group_member(request, group_id):
#     group = Group.objects.get(id=group_id)
#     if request.user != group.admin:
#         return Response({'message': 'Only admin can add members'}, status=status.HTTP_403_FORBIDDEN)
#     user = User.objects.get(id=request.data['user_id'])
#     group.participants.add(user)
#     group.save()
#     return Response({'message': 'User added to group'}, status=status.HTTP_200_OK)

def add_group_member(request, group_id):
    try:
        user_id = request.data.get('user_id')  # Use get to avoid KeyError
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        group.participants.add(user)  # Assuming you have a many-to-many relationship
        return Response({'message': 'User added to group'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({'error': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def send_group_message(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.user not in group.participants.all():
        return Response({'message': 'You are not a member of this group'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data
    data['sender'] = request.user.id  # Set the sender as the current user
    data['group'] = group_id  # Set the group id
    
    serializer = GroupMessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_group_messages(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.user not in group.participants.all():
        return Response({'message': 'You are not a member of this group'}, status=status.HTTP_403_FORBIDDEN)
    messages = GroupMessage.objects.filter(group=group)
    serializer = GroupMessageSerializer(instance=messages, many=True)
    return Response(serializer.data)

# Event Views



@api_view(['POST'])
def create_event(request):
    data = request.data.copy()  # Create a copy of the data
    if request.user.is_authenticated:
        data['creator'] = request.user.id  # Set the creator to the current user if authenticated

    serializer = EventSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def join_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if EventParticipant.objects.filter(event=event, participant=request.user).exists():
        return Response({'message': 'You have already joined this event'}, status=status.HTTP_400_BAD_REQUEST)
    EventParticipant.objects.create(event=event, participant=request.user)
    return Response({'message': 'You have joined the event'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_event_participants(request, event_id):
    event = Event.objects.get(id=event_id)
    participants = EventParticipant.objects.filter(event=event)
    serializer = EventParticipantSerializer(instance=participants, many=True)
    return Response(serializer.data)