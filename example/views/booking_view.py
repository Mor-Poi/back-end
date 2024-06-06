from django.http import *
from bson import ObjectId
from datetime import datetime
from ..serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from db_connection import connect_mongodb
import json 
from rest_framework.permissions import IsAuthenticated
from api.utils import send_booking_ref_to_client

# booking rest api
class BookingView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        db = connect_mongodb()
        booking_collection = db["booking"]
        checklist_collection = db["checklist"]
        school_collection = db["school"]
        # send_booking_ref_to_client("123", ['leonali0329@gmail.com'])

        # Fetch all booking documents
        booking_documents = list(booking_collection.find())

        # Enrich each booking document with checklist and school details
        enriched_bookings = []
        for booking in booking_documents:
            # If checklist_id exists, fetch the checklist document
            if "checklist_id" in booking and booking["checklist_id"]:
                checklist_id = ObjectId(booking["checklist_id"])
                checklist_document = checklist_collection.find_one(
                    {"_id": checklist_id}
                )
                if checklist_document:
                    # Include the checklist details directly in the booking document
                    booking["checklist"] = checklist_document

            # If school_id exists, fetch the school document
            if "school_id" in booking and booking["school_id"]:
                school_id = ObjectId(booking["school_id"])
                school_document = school_collection.find_one({"_id": school_id})
                if school_document:
                    # Include the school details directly in the booking document
                    booking["school"] = school_document

            enriched_bookings.append(booking)

        # Serialize the enriched booking documents
        serializer = BookSerializer(enriched_bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        db = connect_mongodb()
        booking_collection = db["booking"]
        checklist_collection = db["checklist"]
        school_collection = db["school"]
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Insert data into MongoDB
            new_data = serializer.validated_data
            if "checklist_id" in request.data:
                checklist_id = ObjectId(request.data["checklist_id"])
                new_data["checklist_id"] = checklist_id
                checklist_document = checklist_collection.find_one(
                    {"_id": checklist_id}
                )
                if not checklist_document:
                    return Response(
                        {"error": "checklist not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            if "school_id" in request.data:
                school_id = ObjectId(request.data["school_id"])
                new_data["school_id"] = school_id
                school_document = school_collection.find_one({"_id": school_id})
                if not school_document:
                    return Response(
                        {"error": "school not found"}, status=status.HTTP_404_NOT_FOUND
                    )

            result = booking_collection.insert_one(new_data)
            # print(result)
            # Optionally add the MongoDB ID to the response
            new_data["_id"] = str(result.inserted_id)
            response_data = {**new_data, "_id": str(result.inserted_id)}
            # Convert ObjectIds to strings for JSON serialization
            if "school_id" in response_data:
                response_data["checklist_id"] = str(response_data["checklist_id"])
            if "school_id" in response_data:
                response_data["school_id"] = str(response_data["school_id"])
            if booking_collection.find_one({"_id": result.inserted_id}):
                school_id = ObjectId(request.data["school_id"])
                school_email = school_collection.find_one({"_id": school_id})["email"]
                send_booking_ref_to_client(
                    str(result.inserted_id),
                    [school_email],
                    "We have received your booking request. You will recive a new email when the team confirms the booking.",
                    "Science Gallery Received Booking Request",
                )

            # response_data = json.dumps(new_data, default=str)
            return Response(response_data, status=status.HTTP_201_CREATED)
        print("Validation Failed:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingViewID(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return Response(
                {"error": "PUT method expects an id"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        db = connect_mongodb()
        booking_collection = db["booking"]
        checklist_collection = db["checklist"]
        school_collection = db["school"]

        # Find the booking document by _id
        booking_id = ObjectId(kwargs["id"])
        booking_document = booking_collection.find_one({"_id": booking_id})

        if booking_document:
            if "checklist_id" in booking_document:
                checklist_id = ObjectId(booking_document["checklist_id"])
                checklist_document = checklist_collection.find_one(
                    {"_id": checklist_id}
                )
                booking_document["checklist"] = checklist_document

            if "school_id" in booking_document:
                school_id = ObjectId(booking_document["school_id"])
                school_document = school_collection.find_one({"_id": school_id})
                booking_document["school"] = school_document

            serializer = BookSerializer(booking_document)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If the booking document doesn't exist, return an error
        return Response(
            {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return Response(
                {"error": "PUT method expects an id"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        db = connect_mongodb()
        collection = db["booking"]
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            new_data = serializer.validated_data
            booking_id = kwargs["id"]

            try:
                booking_document = collection.find_one({"_id": ObjectId(booking_id)})

                if not booking_document:
                    return Response(
                        {"error": "No record found with the specified ID"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                if "school_id" in new_data:
                    try:
                        new_data["school_id"] = ObjectId(new_data["school_id"])
                    except Exception:
                        return Response(
                            {"error": "Invalid school_id format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                if "checklist_id" in new_data:
                    try:
                        new_data["checklist_id"] = ObjectId(new_data["checklist_id"])
                    except Exception:
                        return Response(
                            {"error": "Invalid checklist_id format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                update_result = collection.update_one(
                    {"_id": ObjectId(booking_id)}, {"$set": new_data}
                )

                if (
                    booking_document["status"] != new_data["status"]
                    and new_data["status"] == "Processing"
                    and booking_document["status"] == "Pending"
                ):
                    school_collection = db["school"]
                    school_id = new_data["school_id"]
                    school_info = school_collection.find_one({"_id": school_id})

                    if school_info:
                        school_email = school_info["email"]
                        send_booking_ref_to_client(
                            booking_id,
                            [school_email],
                            "Thank you for your patience. We have confirmed your booking.",
                            "Science Gallery Booking Confirmation",
                        )

                return Response(
                    {
                        "status": "success",
                        "id": booking_id,
                        "updated": update_result.modified_count,
                    },
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return Response(
                {"error": "DELETE method expects an id"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        db = connect_mongodb()
        booking_collection = db["booking"]
        checklist_collection = db["checklist"]
        school_collection = db["school"]

        try:
            booking_id = ObjectId(kwargs["id"])
        except Exception:
            return Response(
                {"error": "Invalid booking ID format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking_document = booking_collection.find_one({"_id": booking_id})

        if not booking_document:
            return Response(
                {"error": "No booking record found with the specified ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            school_id = ObjectId(booking_document.get("school_id"))
            checklist_id = ObjectId(booking_document.get("checklist_id"))
        except Exception:
            return Response(
                {
                    "error": "Invalid school_id or checklist_id format in booking document"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = db.client.start_session()
        try:
            with session.start_transaction():
                # Delete the school document
                school_delete = school_collection.delete_one(
                    {"_id": school_id}, session=session
                )
                if school_delete.deleted_count == 0:
                    raise Exception("No record found with the specified school ID")

                # Delete the checklist document
                checklist_delete = checklist_collection.delete_one(
                    {"_id": checklist_id}, session=session
                )
                if checklist_delete.deleted_count == 0:
                    raise Exception("No record found with the specified checklist ID")

                # Delete the booking document itself
                booking_delete = booking_collection.delete_one(
                    {"_id": booking_id}, session=session
                )
                if booking_delete.deleted_count == 0:
                    raise Exception("Failed to delete the booking record")

            return Response(
                {
                    "status": "success",
                    "school_deleted": school_delete.deleted_count,
                    "checklist_deleted": checklist_delete.deleted_count,
                    "booking_deleted": booking_delete.deleted_count,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            session.end_session()
