import json


class FileInteraction:
    @staticmethod
    def read_info(path):
        with open(path, "r") as file:
            try:
                file_data = json.load(file)
            except ValueError:
                return {}
            return file_data

    @staticmethod
    def save_info(path, data):
        with open(path, mode="w") as file:
            json.dump(data, file)
