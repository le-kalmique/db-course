from models.dbModel import DbModel


class Dish(DbModel):
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

        self.price = {
            'type': 'number',
            'value': None
        }

        self.restaurant_id = {
            'type': 'number',
            'value': None
        }
