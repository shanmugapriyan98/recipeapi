from rest_framework import serializers
from .models import Message

class MessageSerializers(serializers.ModelSerializer):

  name = serializers.CharField(max_length=50, required=True)
  subject = serializers.CharField(max_length=100, required=True)
  message = serializers.CharField(max_length=1000, required=True)

  def create(self, validated_data):
    return Message.objects.create(
      name = validated_data.get('name'),
      subject = validated_data.get('subject'),
      message = validated_data.get('message')
    )

  def update(self, instance, validated_data):
    instance.name = validated_data.get('name', instance.name)
    instance.subject = validated_data.get('subject', instance.message)
    instance.message = validated_data.get('message', instance.message)
    instance.save()
    return instance

  class Meta:
    model = Message
    fields = (
      'id',
      'name',
      'subject',
      'message'
    )