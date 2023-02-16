import json


class Template:
    def __init__(self):
        with open("templates.json", "r") as file:
            data = json.load(file)
            for key, value in data.items():
                setattr(self, key, value)


TEMPLATE = Template()
