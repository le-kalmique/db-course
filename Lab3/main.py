from db import session, recreate_database
from modelView import EntityView
from CUI.constructor import CUI

from models.User import User
from models.Order import Order
from models.Deliverymen import Deliverymen
from models.Dish import Dish
from models.Restaurant import Restaurant

#recreate_database()

if __name__ == '__main__':
    cui = CUI('lab3')
    cui.addField('Users', lambda: EntityView(User).run())
    cui.addField('Deliverymen', lambda: EntityView(Deliverymen).run())
    cui.addField('Orders', lambda: EntityView(Order).run())
    cui.addField('Dishes', lambda: EntityView(Dish).run())
    cui.addField('Restaurants', lambda: EntityView(Restaurant).run())
    cui.run()
    session.close()


