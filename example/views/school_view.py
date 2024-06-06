from rest_framework.views import APIView
from django.http import *
from bson import ObjectId
from datetime import datetime
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from db_connection import connect_mongodb
import json 
from rest_framework.permissions import IsAuthenticated

class SchoolView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        db = connect_mongodb()
        # Perform some MongoDB operations, e.g., find one document
        collection = db['school']
        documents = list(collection.find())
        serializer = SchoolSerializer(documents, many=True)
        return Response(serializer.data)

    
    def post(self, request, *args, **kwargs):
        collection = connect_mongodb()['school']
        print(request.data)
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            # Insert data into MongoDB
            new_data = serializer.validated_data
            result = collection.insert_one(new_data)
            # Optionally add the MongoDB ID to the response
            new_data['_id'] = str(result.inserted_id)
            # response_data = json.dumps(new_data, default=str)
            return Response(new_data, status=status.HTTP_201_CREATED)
        print("Validation Failed:", serializer.errors)
        print("#######")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolViewID(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return Response({'error': 'PUT method expects an id'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        db = connect_mongodb()
        collection = db['school']
        document = collection.find_one({'_id': ObjectId(kwargs['id'])})
        serializer = SchoolSerializer(document)
        if document:
            return Response(serializer.data)
        else:
            return Response({'error': 'School not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return Response({'error': 'PUT method expects an id'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        db = connect_mongodb()
        collection = db['school']
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            # Insert data into MongoDB
            new_data = serializer.validated_data
           
            update_result = collection.update_one({'_id': ObjectId(kwargs['id'])}, {'$set': new_data})
            
            if update_result.matched_count == 0:
                return Response({'error': 'No record found with the specified ID'},status=status.HTTP_404_NOT_FOUND)
            return Response({'status': 'success', 'id': kwargs['id'], 'updated': update_result.modified_count}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return Response({'error': 'DELETE method expects an id'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        db = connect_mongodb()
        collection = db['school']
        delete_result = collection.delete_one({'_id': ObjectId(kwargs['id'])})

        if delete_result.deleted_count == 0:
            return Response({'error': 'No record found with the specified ID'},status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'success', 'id': kwargs['id']}, status=status.HTTP_200_OK)


