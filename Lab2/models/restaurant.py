from models.dbModel import DbModel


class Restaurant(DbModel):
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

        self.description = {
            'type': 'string',
            'value': None,
            'not null': False
        }

        self.address = {
            'type': 'string',
            'value': None
        }
