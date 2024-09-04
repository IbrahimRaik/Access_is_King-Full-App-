from user_auth.models import User
from user_auth.serializers import UserSerializer
from Chat.models import Conversation, Message, Group, GroupMessage, Event, EventParticipant

from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    # sender = serializers.ForeignKey
    class Meta:
        model = Message
        exclude = ('conversation_id',)


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = UserSerializer()
    receiver = UserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message)


class ConversationSerializer(serializers.ModelSerializer):
    initiator = UserSerializer()
    receiver = UserSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'message_set']


class ConversationIDSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=0)
    initiator = UserSerializer()
    receiver = UserSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['id','initiator', 'receiver', 'message_set']



class GroupSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    participants = UserSerializer(many=True)
    

    class Meta:
        model = Group
        fields = ['id', 'name', 'admin', 'participants', 'created_at']

# class GroupMessageSerializer(serializers.ModelSerializer):
#     sender = UserSerializer()

#     class Meta:
#         model = GroupMessage
#         fields = ['id', 'sender', 'text', 'attachment', 'timestamp']

class GroupMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Ensure 'sender' is read-only
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = GroupMessage
        fields = ['id', 'sender', 'text', 'attachment', 'group', 'timestamp']
        extra_kwargs = {
            'attachment': {'required': False, 'allow_null': True}  # Make 'attachment' optional
        }




class EventSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'creator', 'participants', 'start_time', 'end_time', 'created_at']

class EventParticipantSerializer(serializers.ModelSerializer):
    participant = UserSerializer()

    class Meta:
        model = EventParticipant
        fields = ['id', 'event', 'participant', 'joined_at']