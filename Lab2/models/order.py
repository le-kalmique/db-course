from models.dbModel import DbModel


class Order(DbModel):
    def __init__(self):
        self.id = {
            'type': 'number',
            'value': "DEFAULT",
            'not null': False
        }

        self.user_id = {
            'type': 'number',
            'value': None
        }

        self.deliverymen_id = {
            'type': 'number',
            'value': None
        }
