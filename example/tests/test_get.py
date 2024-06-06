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

    def get_all(self, uri):
        # Retrieve the document

        response = self.client.get(reverse(uri))

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_by_id(self, id, uri ):
        # Retrieve the document
        kwargs = {'id': id}
        response = self.client.get(reverse(uri, kwargs=kwargs), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_by_id_error(self, uri):
        # Retrieve the document
        kwargs = {'id': '6617d801a8f2c8521a42cc2d'}
        # Wrong id
        response = self.client.get(reverse(uri, kwargs=kwargs), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_get_api(self):
        names = ['school', 'checklist', 'template', 'booking']

        for i in names:
            self.get_all(i)


    def test_get_by_id(self):
        id_names = {'school_id': '6617d801a8f2c8521a42cc2c', 'checklist_id': '6617d802a8f2c8521a42cc30', 
                    'template_id': '6617d801a8f2c8521a42cc2e', 'booking_id':'6617d803a8f2c8521a42cc32'}
        for name, id in id_names.items():
            self.get_by_id(id, name)
            self.get_by_id_error(name)