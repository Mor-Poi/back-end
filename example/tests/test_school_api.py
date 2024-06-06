
# from unittest.mock import patch, MagicMock
# from bson.objectid import ObjectId
# from django.conf import settings
# from pymongo import MongoClient

# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient

# from faker import Faker




# class SchoolAPITests(APITestCase):
#     def _fixture_teardown(self):
#         pass  # Override to prevent Django from trying to tear down the databases

#     def setUp(self):
#         self.mock_db, self.mock_collection = self.setup_mock_database()

#     def tearDown(self):
#         self.mock_db, self.mock_collection = None, None

#     def setup_mock_database(self):
#         mock_db = MagicMock()
#         mock_collection = MagicMock()
#         mock_db.__getitem__.return_value = mock_collection
#         return mock_db, mock_collection


#     @patch('api.views.school_view.connect_mongodb')
#     def test_get_schools(self, mock_connect_mongodb):
#         # Setup mock
#         mock_connect_mongodb.return_value = self.mock_db


#         fake = Faker()
#         mock_schools = []
#         # Generate 10 fake school records
#         for _ in range(10):
#             school = {
#                 'name': fake.company(),
#                 'studentYear': fake.random_int(min=2000, max=2025),
#                 'numStudentAttended': fake.random_int(min=50, max=500),
#                 'numStudentRegistered': fake.random_int(min=50, max=500),
#                 'hourRegistered': fake.random_int(min=100, max=500),
#                 'hourAttended': fake.random_int(min=50, max=400),
#                 'lowSES': fake.boolean(),
#                 'allergy': fake.sentence(),
#                 'contactFirstName': fake.first_name(),
#                 'contactLastName': fake.last_name(),
#                 'email': fake.email(),
#                 'phone': fake.phone_number(),
#             }
#             mock_schools.append(school)

#         self.mock_collection.find.return_value = mock_schools
#         # Execute
#         response = self.client.get(reverse('school'))  # Use the actual name of your URL here

#         # Verify
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 10)  # Ensure 10 schools are returned
#         mock_connect_mongodb.assert_called_once()

#     @patch('api.views.school_view.connect_mongodb')
#     def test_create_school(self, mock_connect_mongodb):
#         # Setup mock
#         mock_connect_mongodb.return_value = self.mock_db
#         mock_inserted_id = ObjectId()
#         # Setup the insert_one to simulate MongoDB's insert and return an inserted_id
#         self.mock_collection.insert_one.return_value = MagicMock(inserted_id=mock_inserted_id)

#         # Data to be sent in the request
#         school_data = {
#             'name': 'Unit Test College',
#             'studentYear': 2023,
#             'numStudentAttended': 100,
#             'numStudentRegistered': 120,
#             'hourRegistered': 150,
#             'hourAttended': 130,
#             'lowSES': False,
#             'allergy': 'None',
#             'contactFirstName': 'Mark',
#             'contactLastName': 'Williams',
#             'email': 'mark.w@example.com',
#             'phone': '1234567890'
#         }


#         # Execute
#         response = self.client.post(reverse('school'), school_data, format='json')  # Use the actual name of your URL here

#         # Verify
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         mock_connect_mongodb.assert_called_once()
#         # Add the _id field to the school_data for assertion
#         school_data['_id'] = str(mock_inserted_id)

#         self.mock_collection.insert_one.assert_called_with(school_data)
#         self.assertIn('_id', response.data)  # Ensure an ID is included in the response

# class SchoolViewIDTestCase(APITestCase):
#     def _fixture_teardown(self):
#         pass  # Override to prevent Django from trying to tear down the databases

#     def setUp(self):
#         self.mock_db, self.mock_collection = self.setup_mock_database()

#     def tearDown(self):
#         self.mock_db, self.mock_collection = None, None

#     def setup_mock_database(self):
#         mock_db = MagicMock()
#         mock_collection = MagicMock()
#         mock_db.__getitem__.return_value = mock_collection
#         return mock_db, mock_collection

#     @patch('api.views.school_view.connect_mongodb')
#     def test_get_existing_document(self, mock_connect_mongodb):
#         mock_connect_mongodb.return_value = self.mock_db
#         fake = Faker()
#         mock_school = {
#             'name': fake.company(),
#             'studentYear': fake.random_int(min=2000, max=2025),
#             'numStudentAttended': fake.random_int(min=50, max=500),
#             'numStudentRegistered': fake.random_int(min=50, max=500),
#             'hourRegistered': fake.random_int(min=100, max=500),
#             'hourAttended': fake.random_int(min=50, max=400),
#             'lowSES': fake.boolean(),
#             'allergy': fake.sentence(),
#             'contactFirstName': fake.first_name(),
#             'contactLastName': fake.last_name(),
#             'email': fake.email(),
#             'phone': fake.phone_number(),
#         }

#         # Mock the find_one method to return a document
#         mock_id = ObjectId()
#         self.mock_collection.find_one.return_value = mock_school

#         # Mock the request kwargs
#         kwargs = {'id': str(mock_id)}

#         # Instantiate the view and call the get method

#         response = self.client.get(reverse('school_id', kwargs=kwargs))

#         # Assert the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, mock_school)

#     @patch('api.views.school_view.connect_mongodb')
#     def test_get_non_existing_document(self, mock_connect_mongodb):
#         mock_connect_mongodb.return_value = self.mock_db

#         # Mock the find_one method to return None
#         self.mock_collection.find_one.return_value = None

#         # Mock the request kwargs
#         kwargs = {'id': '6027ac12b268d33b9982f8e4'}

#         # Instantiate the view and call the get method
#         response = self.client.get(reverse('school_id', kwargs=kwargs))


#         # Assert the response
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     @patch('api.views.school_view.connect_mongodb')
#     def test_put_existing_document(self, mock_connect_mongodb):
#         mock_connect_mongodb.return_value = self.mock_db


#         # Mock the update_one method to return a matched_count of 1
#         self.mock_collection.update_one.return_value.matched_count = 1
#         self.mock_collection.update_one.return_value.modified_count = 1


#         # Mock the request data
#         kwargs = {'id': '6027ac12b268d33b9982f8e4'}
#         #fake = Faker()
#         request_data = {
#             'name': 'Example 2 School',
#             'studentYear': 2022,
#             'numStudentAttended': 100,
#             'numStudentRegistered': 200,
#             'hourRegistered': 300,
#             'hourAttended': 150,
#             'lowSES': False,
#             'allergy': 'None',
#             'contactFirstName': 'John',
#             'contactLastName': 'Doe',
#             'email': 'john.doe@example.com',
#             'phone': '123-456-7890',
#         }


#         # Instantiate the view and call the put method
#         response = self.client.put(reverse('school_id', kwargs=kwargs), data=request_data, format='json')
#         # Assert the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     @patch('api.views.school_view.connect_mongodb')
#     def test_put_non_existing_document(self, mock_connect_mongodb):
#         mock_connect_mongodb.return_value = self.mock_db
#         # Mock the update_one method to return a matched_count of 0
#         self.mock_collection.update_one.return_value.matched_count = 0

#         # Mock the request data
#         kwargs = {'id': '6027ac12b268d33b9982f8e4'}
#         fake = Faker()
#         request_data = {
#             'name': fake.company(),
#             'studentYear': fake.random_int(min=2000, max=2025),
#             'numStudentAttended': fake.random_int(min=50, max=500),
#             'numStudentRegistered': fake.random_int(min=50, max=500),
#             'hourRegistered': fake.random_int(min=100, max=500),
#             'hourAttended': fake.random_int(min=50, max=400),
#             'lowSES': fake.boolean(),
#             'allergy': fake.sentence(),
#             'contactFirstName': fake.first_name(),
#             'contactLastName': fake.last_name(),
#             'email': fake.email(),
#             'phone': fake.phone_number(),
#         }

#         # Instantiate the view and call the put method
#         response = self.client.put(reverse('school_id', kwargs=kwargs), data=request_data, format='json')

#         # Assert the response
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     @patch('api.views.school_view.connect_mongodb')
#     def test_delete_existing_document(self, mock_connect_mongodb):
#         mock_connect_mongodb.return_value = self.mock_db

#         # Mock the delete_one method to return a deleted_count of 1
#         self.mock_collection.delete_one.return_value.deleted_count = 1

#         # Mock the request data
#         kwargs = {'id': '6027ac12b268d33b9982f8e4'}

#         # Instantiate the view and call the delete method
#         response = self.client.delete(reverse('school_id', kwargs=kwargs))

#         # Assert the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     @patch('api.views.school_view.connect_mongodb')
#     def test_delete_non_existing_document(self, mock_connect_mongodb):
#         mock_connect_mongodb.return_value = self.mock_db

#         # Mock the delete_one method to return a deleted_count of 0
#         self.mock_collection.delete_one.return_value.deleted_count = 0

#         # Mock the request data
#         kwargs = {'id': '6027ac12b268d33b9982f8e4'}

#         # Instantiate the view and call the delete method
#         response = self.client.delete(reverse('school_id', kwargs=kwargs))

#         # Assert the response
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)