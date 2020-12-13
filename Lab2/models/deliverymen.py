from models.dbModel import DbModel


class Deliverymen(DbModel):
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

        self.surname = {
            'type': 'string',
            'value': None
        }

        self.rating = {
            'type': 'number',
            'value': None
        }
