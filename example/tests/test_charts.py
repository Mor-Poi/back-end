from pymongo import MongoClient
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


from django.conf import settings
# this test is valid for 'test' db not 'unit_test' db, since 'unit_test' db has not been updated

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

    def test_chart_1(self):
        response = self.client.get(reverse('chart_1'), format='json')
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_chart_2(self):
        response = self.client.get(reverse('chart_2'), format='json')
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_chart_3(self):
        response = self.client.get(reverse('chart_3'), format='json')
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_chart_4(self):
        response = self.client.get(reverse('chart_4'), format='json')
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)