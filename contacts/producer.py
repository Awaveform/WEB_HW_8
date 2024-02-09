import argparse
import pika
import json

from contacts.contact import Contact
from contacts.load_data import write_to_db
from contacts.rabbit_connect import make_channel
from db_connect import connect_mongo_db



channel, connection = make_channel()

EXCHANGE_NAME = "contacts_task"
SMS_QUEUE_NAME = "sms_queue"
EMAIL_QUEUE_NAME = "email_queue"

channel.exchange_declare(exchange="contacts_task", exchange_type="direct")

channel.queue_declare(queue=EMAIL_QUEUE_NAME, durable=True)
channel.queue_declare(queue=SMS_QUEUE_NAME, durable=True)

channel.queue_bind(exchange=EXCHANGE_NAME, queue=EMAIL_QUEUE_NAME)
channel.queue_bind(exchange=EXCHANGE_NAME, queue=SMS_QUEUE_NAME)

parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

parser.add_argument("-n", "--number", default=10)
args = parser.parse_args()


def main():
    connect_mongo_db()
    write_to_db(contacts_num=int(args.number))
    contacts = Contact.objects().all()
    for i, contact in enumerate(contacts):
        message = {
            "fullname": contact.fullname,
            "email": contact.email,
            "phone": contact.phone,
            "born_date": contact.born_date.strftime("%Y-%m-%d"),
            "born_location": contact.born_location,
            "is_sent_msg": contact.is_sent_msg,
            "preferred_connect_channel": contact.preferred_connect_channel,
        }
        queue_name = EMAIL_QUEUE_NAME
        if contact.preferred_connect_channel == "phone":
            queue_name = SMS_QUEUE_NAME

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=queue_name,
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    connection.close()


if __name__ == "__main__":
    main()
