from rest_framework import serializers
from .models import Recipe

class RecipeSerializers(serializers.ModelSerializer):
  name = serializers.CharField(max_length=50, required=True)
  info = serializers.CharField(max_length=1000, required=True)

  def create(self, validated_data):
    return Recipe.objects.create(
      name = validated_data.get('name'),
      info = validated_data.get('info')
    )

  def update(self, instance, validated_data):
    instance.name = validated_data.get('name', instance.name)
    instance.info = validated_data.get('info', instance.info)
    instance.save()
    return instance

  class Meta:
    model = Recipe
    fields = (
      'id',
      'name',
      'info'
    )