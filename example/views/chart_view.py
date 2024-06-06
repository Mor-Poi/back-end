from rest_framework.views import APIView
from django.http import *
from bson import ObjectId
from datetime import datetime
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from db_connection import connect_mongodb
import json


# analysis charts api
class ChartOneView(APIView):
    def get(self, request, *args, **kwargs):
        db = connect_mongodb()
        booking_collection = db["booking"]

        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "school",
                        "localField": "school_id",
                        "foreignField": "_id",
                        "as": "school_info",
                    }
                },
                {
                    "$unwind": {
                        "path": "$school_info",
                        "preserveNullAndEmptyArrays": False,
                    }
                },
                {
                    "$project": {
                        "month": {"$month": "$startTime"},
                        "numStudentAttended": "$school_info.numStudentAttended",
                        "numStudentRegistered": "$school_info.numStudentRegistered",
                    }
                },
                {
                    "$group": {
                        "_id": "$month",
                        "total_participants": {"$sum": "$numStudentAttended"},
                        "total_registrants": {"$sum": "$numStudentRegistered"},
                    }
                },
                {"$sort": {"_id": 1}},
            ]

            result = list(booking_collection.aggregate(pipeline))
            participants = [0] * 12
            registrants = [0] * 12

            for data in result:
                month_index = data["_id"] - 1
                participants[month_index] = data.get("total_participants", 0)
                registrants[month_index] = data.get("total_registrants", 0)

            data = {"participants": participants, "registrants": registrants}

            serializer = ChartOneSerializer(data=data)

            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChartTwoView(APIView):
    def get(self, request, *args, **kwargs):
        db = connect_mongodb()
        booking_collection = db["booking"]

        pipeline = [
            {
                "$lookup": {
                    "from": "school",
                    "localField": "school_id",
                    "foreignField": "_id",
                    "as": "school_info",
                }
            },
            {"$unwind": "$school_info"},
            {
                "$group": {
                    "_id": {
                        "stream": "$programStream",
                        "term": "$term",
                    },
                    "total_students": {"$sum": "$school_info.numStudentAttended"},
                }
            },
            {
                "$group": {
                    "_id": "$_id.stream",
                    "terms": {
                        "$push": {"term": "$_id.term", "count": "$total_students"}
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "stream": "$_id",
                    "terms": {
                        "$arrayToObject": {
                            "$map": {
                                "input": "$terms",
                                "as": "term",
                                "in": {
                                    "k": {"$toString": "$$term.term"},
                                    "v": "$$term.count",
                                },
                            }
                        }
                    },
                }
            },
        ]

        result = list(booking_collection.aggregate(pipeline))

        streams_data = {}
        for item in result:
            stream = item["stream"]
            term_data = {str(term): 0 for term in range(1, 5)}
            term_data.update(item["terms"])  # Update with actual data
            ordered_terms = [term_data[str(term)] for term in range(1, 5)]
            streams_data[stream] = ordered_terms

        data = {"streams": streams_data}

        # mock data
        # mock_data = {
        #     "streams": {
        #         "SCOE": [123, 234, 345, 456],
        #         "STEAM": [210, 320, 430, 540],
        #         "NN Tour+ (UN)EXPECTED WORKSHOP + CHICKENOSAURUS WORKSHOP": [
        #             100,
        #             200,
        #             300,
        #             400,
        #         ],
        #         "ART": [150, 250, 350, 450],
        #     }
        # }

        serializer = ChartTwoSerializer(data=data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChartThreeView(APIView):
    def get(self, request, *args, **kwargs):
        db = connect_mongodb()
        booking_collection = db["booking"]
        pipeline = [
            {
                "$lookup": {
                    "from": "school",
                    "localField": "school_id",
                    "foreignField": "_id",
                    "as": "school_info",
                }
            },
            {"$unwind": "$school_info"},
            {
                "$group": {
                    "_id": {"term": "$term", "location": "$location"},
                    "total_students": {"$sum": "$school_info.numStudentAttended"},
                }
            },
            {
                "$group": {
                    "_id": "$_id.location",
                    "terms": {
                        "$push": {"term": "$_id.term", "count": "$total_students"}
                    },
                }
            },
            {"$project": {"_id": 0, "location": "$_id", "terms": 1}},
        ]

        result = list(booking_collection.aggregate(pipeline))

        locations_data = {}
        for item in result:
            location = item["location"]
            term_data = {term: 0 for term in range(1, 5)}

            for term_info in item["terms"]:
                if term_info["term"] in term_data:
                    term_data[term_info["term"]] = term_info["count"]

            terms_data = [term_data[term] for term in sorted(term_data)]
            locations_data[location] = terms_data

        data = {"locations": locations_data}
        print(data)
        # mock data
        mock_data = {
            "locations": {
                "D ROOM1": [100, 200, 300, 400],
                "D ROOM2": [150, 250, 350, 450],
                "D ROOM3": [130, 230, 330, 430],
                "Buxton": [50, 150, 250, 350],
            }
        }

        serializer = ChartThreeSerializer(data=data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChartFourView(APIView):
    def get(self, request, *args, **kwargs):
        db = connect_mongodb()
        booking_collection = db["booking"]

        pipeline = [
            {
                "$lookup": {
                    "from": "school",
                    "localField": "school_id",
                    "foreignField": "_id",
                    "as": "school_info",
                }
            },
            {"$unwind": "$school_info"},
            {
                "$project": {
                    "programStream": 1,
                    "studentYear": "$school_info.studentYear",
                    "numStudentAttended": "$school_info.numStudentAttended",
                }
            },
            {
                "$group": {
                    "_id": {"stream": "$programStream", "year": "$studentYear"},
                    "numStudentAttended": {"$sum": "$numStudentAttended"},
                }
            },
            {
                "$group": {
                    "_id": "$_id.stream",
                    "grades": {
                        "$push": {
                            "year": "$_id.year",
                            "count": "$numStudentAttended",
                        }
                    },
                }
            },
            {"$project": {"_id": 0, "stream": "$_id", "grades": 1}},
        ]

        result = list(booking_collection.aggregate(pipeline))

        grades_by_stream = {}
        for item in result:
            stream = item["stream"]
            grades_dict = {grade["year"]: grade["count"] for grade in item["grades"]}
            grades_by_stream[stream] = grades_dict

        data = {"grades_by_stream": grades_by_stream}

        serializer = ChartFourSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
