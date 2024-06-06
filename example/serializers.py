from django.contrib.auth.models import Group, User
from rest_framework import serializers
from datetime import datetime


class SchoolSerializer(serializers.Serializer):
    id = serializers.CharField(source="_id", read_only=True)
    name = serializers.CharField(max_length=200)
    studentYear = serializers.IntegerField()
    numStudentAttended = serializers.IntegerField(required=False, default=0)
    numStudentRegistered = serializers.IntegerField()
    hourRegistered = serializers.IntegerField(required=False)
    hourAttended = serializers.IntegerField(required=False)
    lowSES = serializers.BooleanField()
    allergy = serializers.CharField(max_length=200,required=False, default = '',allow_blank= True)
    teachingArea = serializers.CharField(max_length=200, required=False, allow_blank=True, default='')
    contactFirstName = serializers.CharField(max_length=200)
    contactLastName = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=200)
    note = serializers.CharField(max_length=2000, allow_blank=True)
    isAccessibility = serializers.BooleanField(default=False)
    isAllergy = serializers.BooleanField(default=False)
    isPartner = serializers.BooleanField(default=False)


class TaskChecklistSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    link = serializers.URLField(max_length=200, allow_blank=True, default="")
    status = serializers.IntegerField(default=0)


class ChecklistSerializer(serializers.Serializer):
    id = serializers.CharField(source="_id", read_only=True)
    name = serializers.CharField(max_length=255)
    task = TaskChecklistSerializer(many=True)


class TaskTemplateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    link = serializers.URLField(max_length=200, allow_blank=True, default="")


class TemplateSerializer(serializers.Serializer):
    id = serializers.CharField(source="_id", read_only=True)
    name = serializers.CharField(max_length=255)
    task = TaskTemplateSerializer(many=True)


class BusSerializer(serializers.Serializer):
    bus_req = serializers.BooleanField(default=False)
    isBooked = serializers.BooleanField(default=False)
    status = serializers.BooleanField(default=False)
    price = serializers.FloatField(default=0)
    date_paid = serializers.DateTimeField(allow_null=True, required=False)
    invoice = serializers.CharField(max_length=255, allow_blank=True, default="")


class BookSerializer(serializers.Serializer):
    id = serializers.CharField(source="_id", read_only=True)
    name = serializers.CharField(max_length=200)
    programStream = serializers.CharField(required=False)
    facilitators = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    event = serializers.CharField()  # Assuming it's a CharField, you may need a related serializer if it's a nested object.
    status = serializers.ChoiceField(choices=['Pending', 'Processing', 'Delivered', 'Canceled'])
    term = serializers.IntegerField(required=False)
    location = serializers.CharField(required = False, allow_blank=True)  # Or serializers.PrimaryKeyRelatedField if it's a relation to another entity.

#     event = (
#         serializers.CharField()
#     )  # Assuming it's a CharField, you may need a related serializer if it's a nested object.
#     status = serializers.ChoiceField(
#         choices=["Pending", "Processing", "Delivered", "Canceled"]
#     )
#     term = serializers.IntegerField(required=False)
#     location = serializers.CharField(
#         required=False, allow_blank=True, default=""
#     )  # Or serializers.PrimaryKeyRelatedField if it's a relation to another entity.

    date = serializers.DateTimeField()
    checklist_id = (
        serializers.CharField()
    )  # Assuming it's a ForeignKey to another model.
    checklist = ChecklistSerializer(
        required=False
    )  # Assuming it's a ForeignKey to another model.
    startTime = serializers.DateTimeField()
    endTime = serializers.DateTimeField()
    module_id = serializers.ListField(
        child=serializers.CharField(max_length=255), allow_empty=True, required=False
    )
    school_id = serializers.CharField()  # Assuming it's a ForeignKey to another model.
    school = SchoolSerializer(
        required=False
    )  # Assuming it's a ForeignKey to another model.
    exibition = serializers.CharField()  # Assuming it's a ForeignKey to another model.

    note = serializers.CharField(max_length=200, allow_blank=True,required=False)  # Assuming this is optional and can be a blank string.
    bus = BusSerializer(default={
    "bus_req": False,
    "isBooked": False,
    "status": False,
    "price": 0.0,
    "date_paid": None,  # Or any default date
    "invoice": ""
})
#     note = serializers.CharField(
#         max_length=200, allow_blank=True, required=False
#     )  # Assuming this is optional and can be a blank string.
#     bus = BusSerializer(
#         default={
#             "bus_req": False,
#             "isBooked": False,
#             "status": 0,
#             "price": 0.0,
#             "date_paid": None,  # Or any default date
#             "invoice": "",
#         }
#     )

    per_student = serializers.IntegerField(default=0)
    expense = serializers.IntegerField(default=0)
    income = serializers.IntegerField(default=0)
    profit = serializers.IntegerField(default=0)


class MiscellaneousSerializer(serializers.Serializer):
    id = serializers.CharField(source="_id", read_only=True)
    module = serializers.ListField(
        child=serializers.CharField(max_length=255), allow_empty=True
    )
    program_stream = serializers.ListField(
        child=serializers.CharField(max_length=255), allow_empty=True
    )
    facilitators = serializers.ListField(
        child=serializers.CharField(max_length=255, allow_blank = True), allow_empty=True
    )
    delivery_location = serializers.ListField(
        child=serializers.CharField(max_length=255, allow_blank = True), allow_empty=True, 
    )
    exhibition = serializers.ListField(
        child=serializers.CharField(max_length=255), allow_empty=True
    )


class ChartOneSerializer(serializers.Serializer):
    participants = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=12,
        max_length=12,
    )
    registrants = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=12,
        max_length=12,
    )


class ChartTwoSerializer(serializers.Serializer):
    streams = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField())
    )


class ChartThreeSerializer(serializers.Serializer):
    locations = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField())
    )


class ChartFourSerializer(serializers.Serializer):
    grades_by_stream = serializers.DictField(
        child=serializers.DictField(child=serializers.IntegerField())
    )
