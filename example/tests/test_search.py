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

    def test_search_query(self):
        # sample query 
        request = {'query': 'geelong'}
        response = self.client.get(reverse('search'), request, format='json')
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_non_exist(self):

        response = self.client.get(reverse('search'), format='json')
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "No query parameter provided")


    
