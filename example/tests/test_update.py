from pymongo import MongoClient
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


from django.conf import settings

class DBTest(APITestCase):
    def _fixture_teardown(self):
        pass  # Override to prevent Django from trying to tear down the databases

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Connect to the test database
        if settings.TESTING:
            # Connect to the actual MongoDB database
            cls.client = MongoClient(host=settings.MONGODB_URI)

        cls.db = cls.client["unit_test"]
        cls.template_collection = cls.db['template']
        cls.book_collection = cls.db['booking']
        cls.checklist_collection = cls.db['checklist']
        cls.school_collection = cls.db['school']

    def update_by_id(self, uri, id, request):
        kwargs = {'id': id}
        response = self.client.put(reverse(uri, kwargs=kwargs), request, format='json')
         # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def update_by_id_bad_request(self, uri, id):
        request = {
            'name': 'Geelong High School',
            'numStudentAttended': 100,
            'numStudentRegistered': 200,
        }


        kwargs = {'id': id}
        response = self.client.put(reverse(uri, kwargs=kwargs), request, format='json')
         # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def update_by_id_not_found(self, uri, id, request):
        kwargs = {'id': '6617d801a8f2c8521a42cc2d'}
        response = self.client.put(reverse(uri, kwargs=kwargs), request, format='json')
         # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_update(self):
        # Insert a document
        school = {
            'name': 'Geelong High School',
            'studentYear': 2023,
            'numStudentAttended': 100,
            'numStudentRegistered': 200,
            'hourRegistered': 300,
            'hourAttended': 150,
            'lowSES': False,
            'allergy': 'None',
            'contactFirstName': 'Mark',
            'contactLastName': 'Williams',
            'email': 'mark.w@example.com',
            'phone': '123-456-7890',
        }

        template = {
            "name": "Partner School Template",
            "task": [
                {
                "name": "Priava",
                "order": 1,
                "link": "https://apac-app.priava.com/api/login/dist/#/"
                },
                {
                "name": "Place bookings...",
                "order": 2
                }]
        }
        checklist = {
            "name": "Partner School Template",
            "task": [
                {
                "name": "Priava",
                "order": 1,
                "link": "https://apac-app.priava.com/api/login/dist/#/"
                },
                {
                "name": "Place bookings...",
                "order": 2
                }]
        }

        booking = {
            "name": "Contemporary Art Fair",
            "event": "Art Fair 2024",
            "status": "Processing",
            "location": "Exhibition Center - Hall A",
            "date": "2024-09-05T09:00:00Z",
            "checklist_id": "6617d802a8f2c8521a42cc30",
            "startTime": "2024-09-05T10:00:00Z",
            "endTime": "2024-09-05T16:00:00Z",
            "school_id": "6617d801a8f2c8521a42cc2c",
            "exibition": "Local Innovators Showcase",
            "note": "Extra chairs needed in the lobby"
        }


        id_names = {'school_id': '6617d801a8f2c8521a42cc2c', 'checklist_id': '6617d802a8f2c8521a42cc30', 
                    'template_id': '6617d801a8f2c8521a42cc2e', 'booking_id':'6617d803a8f2c8521a42cc32'}
        for name, id in id_names.items():
            if name == 'school_id':
                self.update_by_id(name, id, school)
            elif name == 'checklist_id':
                self.update_by_id(name, id, checklist)
            elif name == 'template_id':
                self.update_by_id(name, id, template)
            else:
                self.update_by_id(name, id, booking)


