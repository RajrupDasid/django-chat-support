from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Message
from rest_framework.serializers import ModelSerializer, CharField

class MessageSeializer(ModelSerializer):
    user = CharField(source='user.username',read_only=True)
    recpient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context[
            'request'
        ].user
        recipient = get_object_or_404(
            User, username = validated_data['recipient']['username'])

        msg = Message(recipient=recipient, body=validated_data['body'], user=user)
        msg.save()
        return msg
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)