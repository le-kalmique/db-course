import math
from controllers.userController import UserController
from models.user import User
from CUI.constructor import CUI

class UserView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("User model menu")
        self.userController = UserController()
        self.CUI.addField('Add User', lambda: self.__addUser())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Users', lambda: self.__getUsers())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setMsg('   Please wait! Rows are generating...   ')
            time = self.userController.generateRows(rowsNum)
            self.CUI.setMsg('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setMsg(str(error))

    def __addUser(self):
        try:
            result = self.userController.add()
            if isinstance(result, bool) and not result: raise Exception(' Inccorect values')
            else: self.CUI.setMsg('New User id: ' + str(result))
        except Exception as err:
            self.CUI.setMsg(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getUsers()

    def __getUsers(self):
        usersMenu = CUI('Users')
        self.currentMenu[0] = usersMenu
        try:
            if self.page < math.ceil(self.userController.getCount() / self.per_page):
                usersMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                usersMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            users = self.userController.getAll(self.page, self.per_page)
            for user in users:
                usersMenu.addField(f"<{user.id}> {user.name}", lambda id=user.id: self.__getUser(id))

        except Exception as err:
            usersMenu.setMsg(str(err))
        usersMenu.run('Return to main menu')

    def __updateUser(self, id: int):
        if self.userController.update(id):
            self.currentMenu[1].stop()
            self.__getUser(id)
        else:
            self.currentMenu[1].setMsg('Incorrect update values')

    def __deleteUser(self, id: int):
        self.userController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getUser(self, id: int):
        userMenu = CUI('User menu')
        self.currentMenu[1] = userMenu
        try:
            user: User = self.userController.getById(id)
            values = user.getValues().split(',')
            keys = user.getKeys().split(',')
            for i in range(len(keys)):
                userMenu.addField(keys[i] + ' : ' + values[i])

            userMenu.addField('DELETE', lambda: self.__deleteUser(user.id))
            userMenu.addField('UPDATE', lambda: self.__updateUser(user.id))
            userMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            userMenu.setMsg(str(err))
        userMenu.run(False)

