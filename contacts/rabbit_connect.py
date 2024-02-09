import configparser
import os
from typing import Tuple

import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

config = configparser.ConfigParser()
config.read(os.environ.get("CONFIG_PATH"))

rabbit_user = config.get("RABBIT_MQ", "user")
rabbit_pass = config.get("RABBIT_MQ", "pass")
rabbit_host = config.get("RABBIT_MQ", "host")
rabbit_port = config.get("RABBIT_MQ", "port")


def make_channel() -> Tuple[BlockingChannel, BlockingConnection]:
    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbit_host, port=rabbit_port, credentials=credentials
        )
    )
    channel = connection.channel()
    return channel, connection
