from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import DbmoduleSerializers
from .models import Recipe

# Create your views here.
class DbmoduleView(APIView):
    def get(self, request, id=None):
        if id:
            # If an id is provided in the GET request, retrieve the Todo item by that id
            try:
                # Check if the todo item the user wants to update exists
                queryset = Recipe.objects.get(id=id)
            except Recipe.DoesNotExist:
            # If the todo item does not exist, return an error response
                return Response({'errors': 'This todo item does not exist.'}, status=400)

            # Serialize todo item from Django queryset object to JSON formatted data
            read_serializer = DbmoduleSerializers(queryset)
        
        else:
            # Get all todo items from the database using Django's model ORM
            queryset = Recipe.objects.all()

            # Serialize list of todos item from Django queryset object to JSON formatted data
            read_serializer = DbmoduleSerializers(queryset, many=True)

        # Return a HTTP response object with the list of todo items as JSON
        return Response(read_serializer.data)
    
    def post(self, request):
        # Pass JSON data from user POST request to serializer for validation
        create_serializer = DbmoduleSerializers(data=request.data)

        # Check if user POST data passes validation checks from serializer
        if create_serializer.is_valid():

            # If user data is valid, create a new todo item record in the database
            todo_item_object = create_serializer.save()

            # Serialize the new todo item from a Python object to JSON format
            read_serializer = DbmoduleSerializers(todo_item_object)

            # Return a HTTP response with the newly created todo item data
            return Response(read_serializer.data, status=201)

        # If the users POST data is not valid, return a 400 response with an error message
        return Response(create_serializer.errors, status=400)
