from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import MessageSerializers

# Create your views here.
class RecipeView(APIView):
    
    def post(self, request):
        create_serializer = MessageSerializers(data=request.data)

        # Check if user POST data passes validation checks from serializer
        if create_serializer.is_valid():

            todo_item_object = create_serializer.save()

            read_serializer = MessageSerializers(todo_item_object)

            return Response(read_serializer.data, status=201)

        return Response(create_serializer.errors, status=400)
