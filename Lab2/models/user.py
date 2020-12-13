from models.dbModel import DbModel


class User(DbModel):
    def __init__(self):
        self.id = {
            'type': 'number',
            'value': "DEFAULT",
            'not null': False
        }
        self.name = {
            'type': 'string',
            'value': None
        }

        self.discount = {
            'type': 'number',
            'value': None,
            'not null': False
        }

        self.phone_number = {
            'type': 'string',
            'value': None
        }

        self.email = {
            'type': 'string',
            'value': None
        }