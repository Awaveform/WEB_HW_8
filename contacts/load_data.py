import random
from datetime import datetime, timedelta
from faker import Faker
import mongoengine

from db_connect import connect_mongo_db
from contact import Contact

fake = Faker()
PHONE_LEN = 12


def generate_phone_num(phone_len: int) -> str:
    phone_num = ""
    for i in range(0, phone_len):
        phone_num += str(random.randint(0, 9))
    return phone_num


def write_to_db(contacts_num: int) -> None:
    for i in range(contacts_num):
        random_num = random.randint(10, 30)
        random_phone = generate_phone_num(phone_len=PHONE_LEN)
        connect_channels = ["email", "phone"]
        born_date = (datetime.now() - timedelta(days=random_num * 365)).date()
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=random_phone,
            born_location=fake.country(),
            born_date=born_date,
            preferred_connect_channel=random.choice(connect_channels),
        )
        try:
            contact.save()
        except mongoengine.errors.NotUniqueError:
            pass


if __name__ == "__main__":
    connect_mongo_db()
    write_to_db(contacts_num=10)
