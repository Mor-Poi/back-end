from rest_framework.views import APIView
from django.http import *
from bson import ObjectId
from datetime import datetime
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from db_connection import connect_mongodb
import json 


class MiscellaneousView(APIView):
    def get(self, request, *args, **kwargs):
        db = connect_mongodb()
        # Perform some MongoDB operations, e.g., find one document
        collection = db['miscellaneous']
        document = collection.find()[0]
        serializer = MiscellaneousSerializer(document)
        if document:
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

    
    def post(self, request, *args, **kwargs):
        collection = connect_mongodb()['miscellaneous']
        serializer = MiscellaneousSerializer(data=request.data)
        if serializer.is_valid():
            # Insert data into MongoDB
            new_data = serializer.validated_data
            result = collection.insert_one(new_data)
            # Optionally add the MongoDB ID to the response
            new_data['_id'] = str(result.inserted_id)
            # response_data = json.dumps(new_data, default=str)
            return Response(new_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        db = connect_mongodb()
        collection = db['miscellaneous']
        serializer = MiscellaneousSerializer(data=request.data)
        if serializer.is_valid():
            # Insert data into MongoDB
            new_data = serializer.validated_data

            update_result = collection.update_one({},{'$set': new_data})
            if update_result.matched_count == 0:
                return Response({'error': 'No record found'},status=status.HTTP_404_NOT_FOUND)
            return Response({'status': 'success', 'updated': update_result.modified_count}, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


