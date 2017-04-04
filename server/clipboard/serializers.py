from django.contrib.auth.models import User
from rest_framework import serializers
from clipboard.models import Clip

class ClipSerializer(serializers.ModelSerializer):
    # Using ModelSerializers is just shortcut for Serializers
    # with default create and update
    class Meta:
        model = Clip
        fields = ('id', 'user_id', 'text', 'device')

class UserSerializer(serializers.ModelSerializer):
    clip = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Clip.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'clips')
        
