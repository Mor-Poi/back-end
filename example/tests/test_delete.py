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



    def delete_by_id(self, id, uri ):
        # Retrieve the document
        kwargs = {'id': id}
        response = self.client.delete(reverse(uri, kwargs=kwargs), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_by_id_error(self, uri):
        # Retrieve the document
        kwargs = {'id': '6617d801a8f2c8521a42cc2d'}
        # Wrong id
        response = self.client.delete(reverse(uri, kwargs=kwargs), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_delete_by_id(self):
        """
        CAUTION:
        The test ids must be check manually in MongoDB first and update to the newest id accordingly,
        Once the TEST has ran these documents will be deleted in the database
        """

        id_names = {'school_id': '661e65625170f95b7f05cdd0', 'checklist_id': '661e65635170f95b7f05cdd4', 
                    'template_id': '661e65625170f95b7f05cdd2', 'booking_id':'661e65635170f95b7f05cdd6'}
        for name, id in id_names.items():
            self.delete_by_id(id, name)
            self.delete_by_id_error(name)







	