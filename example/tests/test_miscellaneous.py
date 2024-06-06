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
        cls.misc_collection = cls.db['miscellaneous']

    def test_get_all(self):
        # Retrieve the document

        response = self.client.get(reverse('miscellaneous'))

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        data = {"module":["Access Code","F: Bespoke","TBC","TOUR: Nadine Christensen - Facilitated",
                          "TOUR: Not Natural - Facilitated","VISIT: Ancient Lives - Self-directed",
                          "VISIT: Nadine Christensen - Self-Directed",
                          "W: App It!","W: Design It!",
                          "W: Future Food","W: Mission Control",
                          "W: Sustainable Communities","W: Take Flight"],
                "program_stream":["ART","SCOE","STEAM","STEAM LEARNING EXCURSIONS","STEM CENTRE OF EXCELLENCE"],
                "facilitators":["EB","ER","JC","MC","MelB","MK","Teacher Delivered","TS","XC"],
                "delivery_location":["Buxton","Embedded (25%)","Incursion","Old Quad","SGM: EG, WG","SGM: SGMT","SGM: W2","SGM: W3"],
                "exhibition":["Ancient Lives","Nadine Christensen","Non-Exhibition Linked","Natural"]
                }   
        response = self.client.put(reverse('miscellaneous'), data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_not_valid(self):
        data = {"module":["Access Code","F: Bespoke","TBC","TOUR: Nadine Christensen - Facilitated",
                          "TOUR: Not Natural - Facilitated","VISIT: Ancient Lives - Self-directed",
                          "VISIT: Nadine Christensen - Self-Directed",
                          "W: App It!","W: Design It!",
                          "W: Future Food","W: Mission Control",
                          "W: Sustainable Communities","W: Take Flight"],
            
                }   
        response = self.client.put(reverse('miscellaneous'), data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
