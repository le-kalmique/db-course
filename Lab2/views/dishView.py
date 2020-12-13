import math
from controllers.dishController import DishController
from models.dish import Dish
from CUI.constructor import CUI

class DishView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Dish model menu")
        self.dishController = DishController()
        self.CUI.addField('Add Dish', lambda: self.__addDish())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Dishs', lambda: self.__getDishs())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setMsg('   Please wait! Rows are generating...   ')
            time = self.dishController.generateRows(rowsNum)
            self.CUI.setMsg('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setMsg(str(error))

    def __addDish(self):
        try:
            result = self.dishController.add()
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setMsg('New Dish id: ' + str(result))
        except Exception as err:
            self.CUI.setMsg(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getDishs()

    def __getDishs(self):
        dishsMenu = CUI('Dishs')
        self.currentMenu[0] = dishsMenu
        try:
            if self.page < math.ceil(self.dishController.getCount() / self.per_page):
                dishsMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                dishsMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            dishs = self.dishController.getAll(self.page, self.per_page)
            for dish in dishs:
                dishsMenu.addField(f"<{dish.id}> {dish.name}", lambda id=dish.id: self.__getDish(id))

        except Exception as err:
            dishsMenu.setMsg(str(err))
        dishsMenu.run('Return to main menu')

    def __updateDish(self, id: int):
        if self.dishController.update(id):
            self.currentMenu[1].stop()
            self.__getDish(id)
        else:
            self.currentMenu[1].setMsg('Incorrect update values')

    def __deleteDish(self, id: int):
        self.dishController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getDish(self, id: int):
        dishMenu = CUI('Dish menu')
        self.currentMenu[1] = dishMenu
        try:
            dish: Dish = self.dishController.getById(id)
            values = dish.getValues().split(',')
            keys = dish.getKeys().split(',')
            for i in range(len(keys)):
                dishMenu.addField(keys[i] + ' : ' + values[i])

            dishMenu.addField('DELETE', lambda: self.__deleteDish(dish.id))
            dishMenu.addField('UPDATE', lambda: self.__updateDish(dish.id))
            dishMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            dishMenu.setMsg(str(err))
        dishMenu.run(False)

