from rest_framework import serializers

from .models import Recipe


class DbmoduleSerializers(serializers.ModelSerializer):
  text = serializers.CharField(max_length=1000, required=True)
  name = serializers.CharField(max_length=20, required=True)

  def create(self, validated_data):
    return Recipe.objects.create(
      text = validated_data.get('text'),
      name = validated_data.get('name')
    )

  def update(self, instance, validated_data):
    instance.text = validated_data.get('text', instance.text)
    instance.name = validated_data.get('name', instance.name)
    instance.save()
    return instance

  class Meta:
    model = Recipe
    fields = (
      'id',
      'text', 
      'name'
    )