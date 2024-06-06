from rest_framework.views import APIView
from django.http import *
from bson import ObjectId
from datetime import datetime
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from db_connection import connect_mongodb
import json


class SearchAPIView(APIView):

    def get(self, request):
        db = connect_mongodb()
        booking_collection = db["booking"]
        school_collection = db["school"]

        query_string = request.query_params.get("query", None)
        booking_documents = []
        if query_string:
            try:
                booking_documents = list(
                    booking_collection.find({"_id": ObjectId(query_string)})
                )
            except Exception:
                booking_documents = []

            if not booking_documents:
                print("check booking")
                booking_query = {
                    "$or": [
                        {"programStream": {"$regex": query_string, "$options": "i"}},
                        {"facilitators": {"$regex": query_string, "$options": "i"}},
                        {"exibition": {"$regex": query_string, "$options": "i"}},
                    ]
                }
                booking_documents = list(booking_collection.find(booking_query))

                school_query = {"name": {"$regex": query_string, "$options": "i"}}
                matching_schools = school_collection.find(school_query, {"_id": 1})
                school_ids = [school["_id"] for school in matching_schools]
                if school_ids:
                    bookings_from_schools = list(
                        booking_collection.find({"school_id": {"$in": school_ids}})
                    )
                    booking_documents.extend(bookings_from_schools)

            serializer = BookSerializer(booking_documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "No query parameter provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
