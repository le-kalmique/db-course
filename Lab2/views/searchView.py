import math
import time

from controllers.searchController import SearchController
from CUI.constructor import CUI

class SearchView:
    def __init__(self):
        self.currentMenu = None
        self.page = 1
        self.per_page = 10
        self.min = None
        self.max = None

        self.CUI = CUI("Search menu")
        self.searchController = SearchController()
        self.CUI.addField('Get orders by names', lambda: self.getOrdersByNames())
        self.CUI.addField('Get dishes by user name', lambda: self.getUserDishes())
        self.CUI.addField('Get Restaurants by Deliveryman rating', lambda: self.getRestaurantsDeliverymensByRating())

    def run(self):
        self.CUI.run()

    def getOrdersByNames(self):
        try:
            user_name = input('Enter user name: ')
            if user_name is None or not isinstance(user_name, str):
                raise Exception('')

            deliverymen_name = input('Enter deliverymen name: ')
            if deliverymen_name is None or not isinstance(deliverymen_name, str):
                raise Exception('')

            items = self.searchController.getOrdersByNames(user_name, deliverymen_name)

            if len(items) > 0:
                startTime = time.time()

                self.currentMenu = CUI('Find menu')
                self.currentMenu.addField('Order id   User name   Deliverymen name')
                for item in items:
                    self.currentMenu.addField(str(item[0]) + '  ' + item[1][0] + '  ' + item[2][0])

                endTime = time.time()
                self.currentMenu.setMsg(' Elapsed time: ' + str(endTime - startTime)[:9] + 's')
                self.currentMenu.run()

            else: self.CUI.setMsg('No entries were found')

        except Exception as err:
            self.currentMenu.setMsg('Invalid input! ' + str(err))

    def getUserDishes(self):
        try:
            user_name = input('Enter user name: ')
            if user_name is None or not isinstance(user_name, str):
                raise Exception('')

            items = self.searchController.getUserDishes(user_name)

            if len(items) > 0:
                startTime = time.time()

                self.currentMenu = CUI('Find menu')
                self.currentMenu.addField('User name        Dishes ')
                for item in items:
                    tmp_str = ''
                    for dish in item[1]:
                        tmp_str += dish + ', '
                    self.currentMenu.addField(item[0] + '  ' + tmp_str[:-2])

                endTime = time.time()
                self.currentMenu.setMsg(' Elapsed time: ' + str(endTime - startTime)[:9] + 's')

                self.currentMenu.run()
            else: self.CUI.setMsg('No entries were found')

        except Exception as err:
            self.currentMenu.setMsg('Invalid input! ' + str(err))

    def getRestaurantsDeliverymensByRating(self):
        try:
            minRating = input('Enter min rating value: ')
            if not minRating.isdecimal():
                raise Exception('')

            maxRating = input('Enter max rating value: ')
            if not maxRating.isdecimal():
                raise Exception('')

            restaurant_name = input('Enter restaurant name: ')
            if restaurant_name is None or not isinstance(restaurant_name, str):
                raise Exception('')

            items = self.searchController.getRestaurantsDeliverymensByRating(int(minRating), int(maxRating), restaurant_name)

            if len(items) > 0:
                startTime = time.time()
                self.currentMenu = CUI('Find menu')
                self.currentMenu.addField('Restaurant       Best deliverymen')
                for item in items:
                    tmp_str = ''
                    for i in range(1, 5):
                        tmp_str += item[1][i] + ', '
                    self.currentMenu.addField(str(item[0]) + '    ' + tmp_str[:-2])

                endTime = time.time()
                self.currentMenu.setMsg(' Elapsed time: ' + str(endTime - startTime)[:9] + 's')
                self.currentMenu.run()

            else: self.CUI.setMsg('No entries were found')

        except Exception as err:
            self.currentMenu.setMsg('Invalid input! ' + str(err))