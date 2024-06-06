from pymongo import MongoClient
from django.conf import settings

def connect_mongodb():


    config = settings.DMONGODB_DATABASES['default']
    client = MongoClient(host=config['host'],
                        #  username=config['username'],
                        #  password=config['password'],
                         )
    if settings.TESTING:
        db = client['unit_test']


    else:
        db = client['test']
    return db