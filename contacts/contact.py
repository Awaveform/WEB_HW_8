from mongoengine import *


class Contact(Document):
    fullname = StringField(max_length=200, required=True)
    email = StringField(max_length=200, required=True, unique=True)
    phone = StringField(max_length=15, required=True, unique=True)
    born_date = DateTimeField(required=True)
    born_location = StringField(max_length=300, required=True)
    is_sent_msg = BooleanField(required=True, default=False)
    preferred_connect_channel = StringField(required=True, choices=["phone", "email"])

    meta = {"db_alias": "some_db"}
