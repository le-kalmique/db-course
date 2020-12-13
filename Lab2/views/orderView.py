import math
from controllers.orderController import OrderController
from models.order import Order
from CUI.constructor import CUI

class OrderView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Order model menu")
        self.orderController = OrderController()
        self.CUI.addField('Add Order', lambda: self.__addOrder())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Orders', lambda: self.__getOrders())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setMsg('   Please wait! Rows are generating...   ')
            time = self.orderController.generateRows(rowsNum)
            self.CUI.setMsg('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setMsg(str(error))

    def __addOrder(self):
        try:
            result = self.orderController.add()
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setMsg('New Order id: ' + str(result))
        except Exception as err:
            self.CUI.setMsg(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getOrders()

    def __getOrders(self):
        ordersMenu = CUI('Orders')
        self.currentMenu[0] = ordersMenu
        try:
            if self.page < math.ceil(self.orderController.getCount() / self.per_page):
                ordersMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                ordersMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            orders = self.orderController.getAll(self.page, self.per_page)
            for order in orders:
                ordersMenu.addField(f"<{order.id}>", lambda id=order.id: self.__getOrder(id))

        except Exception as err:
            ordersMenu.setMsg(str(err))
        ordersMenu.run('Return to main menu')

    def __updateOrder(self, id: int):
        if self.orderController.update(id):
            self.currentMenu[1].stop()
            self.__getOrder(id)
        else:
            self.currentMenu[1].setMsg('Incorrect update values')

    def __deleteOrder(self, id: int):
        self.orderController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getOrder(self, id: int):
        orderMenu = CUI('Order menu')
        self.currentMenu[1] = orderMenu
        try:
            order: Order = self.orderController.getById(id)
            values = order.getValues().split(',')
            keys = order.getKeys().split(',')
            for i in range(len(keys)):
                orderMenu.addField(keys[i] + ' : ' + values[i])

            orderMenu.addField('DELETE', lambda: self.__deleteOrder(order.id))
            orderMenu.addField('UPDATE', lambda: self.__updateOrder(order.id))
            orderMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            orderMenu.setMsg(str(err))
        orderMenu.run(False)

