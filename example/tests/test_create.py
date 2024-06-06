from django.test import TestCase
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


    def test_insertion(self):
        #_________________school___________________
        # Insert a document
        request_school = {
            'name': 'Geelong High School',
            'studentYear': 2022,
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
        # Retrieve the document
        old_school = self.school_collection.count_documents({})

        school_response = self.client.post(reverse('school'), request_school, format='json')

        # Assertions
        self.assertEqual(school_response.status_code, status.HTTP_201_CREATED)

        # Count database document
        count_school = self.school_collection.count_documents({})
        self.assertEqual(count_school, old_school+1)
        school_id = school_response.data['_id']

        #____________________end school___________________


        #___________________template________________________

        # Insert a document
        template_data = {
            "name": "Unguided Tour Template",
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
        # Retrieve the document
        old_template = self.template_collection.count_documents({})

        template_response = self.client.post(reverse('template'), template_data, format='json')

        # Assertions
        self.assertEqual(template_response.status_code, status.HTTP_201_CREATED)

        # Count database document
        count_template = self.template_collection.count_documents({})
        self.assertEqual(count_template, old_template+1)
        template_id = template_response.data['_id']
        #___________________end template_____________________


        #___________________end checklist_____________________

        # Retrieve the document
        old_checklist = self.checklist_collection.count_documents({})
        kwargs = {'id': template_id}

        checklist_response = self.client.post(reverse('checklist_id', kwargs=kwargs), format='json')

        # Assertions
        self.assertEqual(checklist_response.status_code, status.HTTP_201_CREATED)

        # Count database document
        count_checklist = self.checklist_collection.count_documents({})
        self.assertEqual(count_checklist, old_checklist+1)
        checklist_id = checklist_response.data['_id']
        #___________________end checklist_____________________

        #___________________booking__________________________

        booking_data = {
            "name": "Contemporary Art Fair",
            "event": "Art Fair 2024",
            "status": "Processing",
            "location": "Exhibition Center - Hall B",
            "date": "2024-09-05T09:00:00Z",
            "checklist_id": checklist_id,
            "startTime": "2024-09-05T10:00:00Z",
            "endTime": "2024-09-05T16:00:00Z",
            "school_id": school_id,
            "exibition": "Local Innovators Showcase",
            "note": "Extra chairs needed in the lobby"
        }
        old_bookings = self.book_collection.count_documents({})

        booking_response = self.client.post(reverse('booking'), booking_data, format='json')

        # Assertions
        self.assertEqual(booking_response.status_code, status.HTTP_201_CREATED)
        # Count database document
        count_bookings = self.book_collection.count_documents({})

        self.assertEqual(count_bookings, old_bookings+1)
        #___________________end booking_____________________

    def test_school_insert_error(self):
        # Insert a document
        request_school = {
            'name': 'Geelong High School',
            'studentYear': 2022
        }
        # Retrieve the document

        school_response = self.client.post(reverse('school'), request_school, format='json')

        # Assertions
        self.assertEqual(school_response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_template_insert_error(self):

        # Insert a document
        template_data = {
            "template_name": "Unguided Tour Template",
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
        # Retrieve the document
        template_response = self.client.post(reverse('template'), template_data, format='json')

        # Assertions
        self.assertEqual(template_response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_checklist_insert_error(self):

        # Retrieve the document
        kwargs = {'id': '6027ac12b268d33b9982f8e4'}
        # Wrong template id
        checklist_response = self.client.post(reverse('checklist_id', kwargs=kwargs), format='json')
        self.assertEqual(checklist_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_booking_insert_error(self):
        booking_data = {
            "name": "Contemporary Art Fair",
            "event": "Art Fair 2024",
            "status": "Processing",
            "location": "Exhibition Center - Hall B",
            "date": "2024-09-05T09:00:00Z",
            "checklist_id": '6027ac12b268d33b9982f8e4',
            "startTime": "2024-09-05T10:00:00Z",
            "endTime": "2024-09-05T16:00:00Z",
            "school_id": '6027ac12b268d33b9982f8e4',
            "exibition": "Local Innovators Showcase",
            "note": "Extra chairs needed in the lobby"
        }

        booking_response = self.client.post(reverse('booking'), booking_data, format='json')

        # Assertions
        self.assertEqual(booking_response.status_code, status.HTTP_404_NOT_FOUND)