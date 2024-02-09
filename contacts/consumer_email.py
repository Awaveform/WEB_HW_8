import json

from contacts.contact import Contact
from db_connect import connect_mongo_db
from contacts.rabbit_connect import make_channel

QUEUE_NAME = "email_queue"
channel, connection = make_channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)


def callback(ch, method, body):
    message = json.loads(body.decode())
    connect_mongo_db()
    contact = Contact.objects(email=message["email"]).first()
    if contact:
        contact.update(is_sent_msg=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)


if __name__ == "__main__":
    channel.start_consuming()
    connection.close()
