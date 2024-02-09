from db_connect import connect_mongo_db
from models import QueryData


METHODS = {
    "name": QueryData.get_quotes_by_name,
    "tag": QueryData.get_quotes_by_tags,
    "tags": QueryData.get_quotes_by_tags,
}


def parse_cli_input(console_input):
    console_attrs = console_input.split(":")
    method = METHODS.get(console_attrs[0])
    arguments = [attr.strip() for attr in console_attrs[1].split(",")]
    return method, arguments


if __name__ == "__main__":
    console_input = input("My command: ")
    while console_input and console_input != "exit":
        connect_mongo_db()
        method, arguments = parse_cli_input(console_input=console_input)
        rows = method(*arguments)
        print(rows)
        console_input = input("My command: ")
