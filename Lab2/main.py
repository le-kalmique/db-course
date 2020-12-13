from views.deliverymenView import DeliverymenView
from views.dishView import DishView
from views.orderView import OrderView
from views.restaurantView import RestaurantView
from views.userView import UserView
from views.searchView import SearchView
from CUI.constructor import CUI

if __name__ == '__main__':
    main = CUI()
    main.addField('Deliverymen', lambda: DeliverymenView().run())
    main.addField('Dish', lambda: DishView().run())
    main.addField('Order', lambda: OrderView().run())
    main.addField('Restaurant', lambda: RestaurantView().run())
    main.addField('User', lambda: UserView().run())
    main.addField('Search menu', lambda: SearchView().run())
    main.run()