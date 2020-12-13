import math
from controllers.deliverymenController import DeliverymenController
from models.deliverymen import Deliverymen
from CUI.constructor import CUI

class DeliverymenView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Deliverymen model menu")
        self.deliverymenController = DeliverymenController()
        self.CUI.addField('Add Deliverymen', lambda: self.__addDeliverymen())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Deliverymen', lambda: self.__getDeliverymens())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setMsg('   Please wait! Rows are generating...   ')
            time = self.deliverymenController.generateRows(rowsNum)
            self.CUI.setMsg('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setMsg(str(error))

    def __addDeliverymen(self):
        try:
            result = self.deliverymenController.add()
            if isinstance(result, bool) and not result: raise Exception('Incorrect values')
            else: self.CUI.setMsg('New Deliverymen id: ' + str(result))
        except Exception as err:
            self.CUI.setMsg(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getDeliverymens()

    def __getDeliverymens(self):
        deliverymensMenu = CUI('Deliverymen')
        self.currentMenu[0] = deliverymensMenu
        try:
            if self.page < math.ceil(self.deliverymenController.getCount() / self.per_page):
                deliverymensMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                deliverymensMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            deliverymens = self.deliverymenController.getAll(self.page, self.per_page)
            for deliverymen in deliverymens:
                deliverymensMenu.addField(f"<{deliverymen.id}> {deliverymen.name}", lambda id=deliverymen.id: self.__getDeliverymen(id))

        except Exception as err:
            deliverymensMenu.setMsg(str(err))
        deliverymensMenu.run('Return to main menu')

    def __updateDeliverymen(self, id: int):
        if self.deliverymenController.update(id):
            self.currentMenu[1].stop()
            self.__getDeliverymen(id)
        else:
            self.currentMenu[1].setMsg('Incorrect update values')

    def __deleteDeliverymen(self, id: int):
        self.deliverymenController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getDeliverymen(self, id: int):
        deliverymenMenu = CUI('Deliverymen menu')
        self.currentMenu[1] = deliverymenMenu
        try:
            deliverymen: Deliverymen = self.deliverymenController.getById(id)
            values = deliverymen.getValues().split(',')
            keys = deliverymen.getKeys().split(',')
            for i in range(len(keys)):
                deliverymenMenu.addField(keys[i] + ' : ' + values[i])

            deliverymenMenu.addField('DELETE', lambda: self.__deleteDeliverymen(deliverymen.id))
            deliverymenMenu.addField('UPDATE', lambda: self.__updateDeliverymen(deliverymen.id))
            deliverymenMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            deliverymenMenu.setMsg(str(err))
        deliverymenMenu.run(False)

