from rest_framework import serializers
from AccessIsKing.models import City , NewComments , NewMessages
import uuid

def generate_unique_code(model):
    while True:
        code = uuid.uuid4().hex[:12].upper()
        if not model.objects.filter(code=code).exists():
            return code

class BaseSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=24, read_only=True)  # Set as read-only here

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.label and request is not None:
            return request.build_absolute_uri(obj.label.url)
        return None

class CitySerializer(BaseSerializer):
    title = serializers.CharField(max_length=1024)
    countryname = serializers.CharField(max_length=1024)
    subtitle = serializers.CharField(max_length=256)
    members = serializers.IntegerField(default=0)
    label = serializers.ImageField(required=False)  # Optional field for image upload

    class Meta:
        model = City
        fields = '__all__'

    def create(self, validated_data):
        # Generate a unique code and add it to the validated_data
        validated_data['code'] = generate_unique_code(self.Meta.model)
        
        # Check if the image is provided and process it accordingly
        label = validated_data.pop('label', None)
        
        # Create the instance using the parent class's create method
        instance = super().create(validated_data)
        
        # If an image is provided, set it to the instance and save it again
        if label:
            instance.label = label
            instance.save()

        return instance

    def to_representation(self, instance):
        # Customize the response data if needed
        representation = super().to_representation(instance)
        representation['label_url'] = self.get_image_url(instance)
        return representation


class NewCommentSerializer(BaseSerializer):
    comments = serializers.CharField()
    media_files = serializers.ImageField(required=False)

    class Meta:
        model = NewComments
        fields = '__all__'

    def create(self, validated_data):
        # Generate a unique code and add it to the validated_data
        validated_data['code'] = generate_unique_code(self.Meta.model)
        
        # Check if media_files is provided and process it accordingly
        media_files = validated_data.pop('media_files', None)
        
        # Create the instance using the parent class's create method
        instance = super().create(validated_data)
        
        # If media_files is provided, set it to the instance and save it again
        if media_files:
            instance.media_files = media_files
            instance.save()

        return instance
    

class NewMessagesSerializer(BaseSerializer):
    new_message = serializers.CharField()

    class Meta:
        model = NewMessages
        fields = '__all__'

    def create(self, validated_data):
        # Generate a unique code and add it to the validated_data
        validated_data['code'] = generate_unique_code(self.Meta.model)
        
        # Create the instance using the parent class's create method
        instance = super().create(validated_data)
        
        # Save the instance
        instance.save()

        return instance