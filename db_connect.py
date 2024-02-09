import os

from mongoengine import connect
import configparser

curr_path = os.path.dirname(os.path.abspath(__file__))
config_path = f"{curr_path}/config.ini"
os.environ.setdefault("CONFIG_PATH", config_path)

config = configparser.ConfigParser()
config.read(config_path)

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")


def connect_mongo_db():
    is_local_connect = os.environ.get("IS_LOCAL", False)
    if is_local_connect:
        return connect(host="localhost", port=27017, alias="some_db", db="test")
    else:
        return connect(
            host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""",
            ssl=True,
            alias="some_db",
        )


if __name__ == "__main__":
    connect_mongo_db()
