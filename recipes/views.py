from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RecipeSerializers
from .models import Recipe

class RecipeView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                queryset = Recipe.objects.get(id=id) # Check if the recipe item exists
            except Recipe.DoesNotExist:
                return Response({'errors': 'This recipe item does not exist.'}, status=400)

            # Serialize recipe item from Django queryset object to JSON formatted data
            read_serializer = RecipeSerializers(queryset)
        
        else:
            queryset = Recipe.objects.all() # Get all recipe items from the database

            # Serialize list of todos item from Django queryset object to JSON formatted data
            read_serializer = RecipeSerializers(queryset, many=True)

        return Response(read_serializer.data)
    
    def post(self, request):
        create_serializer = RecipeSerializers(data=request.data)

        # Check if user POST data passes validation checks from serializer
        if create_serializer.is_valid():
            todo_item_object = create_serializer.save()

            # Serialize the new recipe item from a Python object to JSON format
            read_serializer = RecipeSerializers(todo_item_object)
            return Response(read_serializer.data, status=201)
        
        return Response(create_serializer.errors, status=400)
