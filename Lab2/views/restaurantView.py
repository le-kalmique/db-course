import math
from controllers.restaurantController import RestaurantController
from models.restaurant import Restaurant
from CUI.constructor import CUI

class RestaurantView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Restaurant model menu")
        self.restaurantController = RestaurantController()
        self.CUI.addField('Add Restaurant', lambda: self.__addRestaurant())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Restaurants', lambda: self.__getRestaurants())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setMsg('   Please wait! Rows are generating...   ')
            time = self.restaurantController.generateRows(rowsNum)
            self.CUI.setMsg('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setMsg(str(error))

    def __addRestaurant(self):
        try:
            result = self.restaurantController.add()
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setMsg('New Restaurant id: ' + str(result))
        except Exception as err:
            self.CUI.setMsg(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getRestaurants()

    def __getRestaurants(self):
        restaurantsMenu = CUI('Restaurants')
        self.currentMenu[0] = restaurantsMenu
        try:
            if self.page < math.ceil(self.restaurantController.getCount() / self.per_page):
                restaurantsMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                restaurantsMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            restaurants = self.restaurantController.getAll(self.page, self.per_page)
            for restaurant in restaurants:
                restaurantsMenu.addField(f"<{restaurant.id}> {restaurant.name}", lambda id=restaurant.id: self.__getRestaurant(id))

        except Exception as err:
            restaurantsMenu.setMsg(str(err))
        restaurantsMenu.run('Return to main menu')

    def __updateRestaurant(self, id: int):
        if self.restaurantController.update(id):
            self.currentMenu[1].stop()
            self.__getRestaurant(id)
        else:
            self.currentMenu[1].setMsg('Incorrect update values')

    def __deleteRestaurant(self, id: int):
        self.restaurantController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getRestaurant(self, id: int):
        restaurantMenu = CUI('Restaurant menu')
        self.currentMenu[1] = restaurantMenu
        try:
            restaurant: Restaurant = self.restaurantController.getById(id)
            values = restaurant.getValues().split(',')
            keys = restaurant.getKeys().split(',')
            for i in range(len(keys)):
                restaurantMenu.addField(keys[i] + ' : ' + values[i])

            restaurantMenu.addField('DELETE', lambda: self.__deleteRestaurant(restaurant.id))
            restaurantMenu.addField('UPDATE', lambda: self.__updateRestaurant(restaurant.id))
            restaurantMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            restaurantMenu.setMsg(str(err))
        restaurantMenu.run(False)

