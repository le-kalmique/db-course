import sys
import math
import datetime
import re

import CUI.constructor as console


class DbModel:

    # private:
    def __varSetUpDate(self, key: str, value: str):
        datetime.datetime.strptime(value, "%Y-%m-%d")
        exec("self.%s = \"\'%s\'\"" % (key, value))

    def __varSetUpNumber(self, key: str, value: str):
        if not isinstance(int(value), int): raise Exception("Invalid input")
        exec("self.%s = %i" % (key, int(value)))

    def __varSetUpFloat(self, key: str, value: str):
        if not isinstance(float(value), float): raise Exception("Invalid input")
        exec("self.%s = %f" % (key, float(value)))

    def __varSetUpMoney(self, key: str, value: str):
        if not isinstance(int(value), int): raise Exception("Invalid input")
        exec("self.%s = %i" % (key, math.fabs(int(value))))

    def __varSetUpString(self, key: str, value: str):
        if len(value) < 2: raise Exception
        exec("self.%s = \"\'%s\'\"" % (key, value))

    def __fillValue(self, key: str, type: str, *args):
        value: str = ''
        if len(args) > 0 and isinstance(args[0], str):
            value = args[0]
        else:
            if len(args) is 0:
                value = input(f"Enter {key}: ")
        if len(args) == 0: self.__fillMenu.setMsg('')
        try:
            if '"' in value: raise Exception

            # my ORM types:
            if type == 'string':
                self.__varSetUpString(key, value)

            if type == 'number':
                self.__varSetUpNumber(key, value)

            if type == 'float':
                self.__varSetUpFloat(key, value)

            if type == 'money':
                self.__varSetUpMoney(key, value)

            if type == 'date':
                self.__varSetUpDate(key, value)

            if len(args) == 0: self.__fillMenu.renameField(key, key + f'    ({value})')
        except Exception:
            if len(args) == 0: self.__fillMenu.setMsg(f"ERROR! Incorrect {key} input")

    # public:
    def getKeys(self):
        outputStr = ''
        for key in self.__dict__.keys():
            if key != '_DbModel__fillMenu': outputStr += key + ','
        return outputStr[:-1]

    def getValues(self):
        outputStr = ''
        for item in self.__dict__.values():
            if isinstance(item, dict):
                if item['value'] is None: item['value'] = 'null'
                outputStr += str(item['value']) + ','
            if isinstance(item, str) or isinstance(item, int) or isinstance(item, float): outputStr += str(item) + ','
        return outputStr[:-1]

    def fill(self):
        self.__fillMenu = console.CUI('Fill Entity Menu')
        iters = dict((x, y) for x, y in self.__dict__.items() if x[:2] != '__')
        iters.update(self.__dict__)
        for key, value in iters.items():
            if key != '_DbModel__fillMenu' and key != 'id':
                print(key, value)
                self.__fillMenu.addField(key, lambda key=key, value=value: self.__fillValue(key, value['type']))
        self.__fillMenu.run("Save and return")

    def parse(self, serverResponse: tuple):
        try:
            if serverResponse.__len__() != self.__dict__.keys().__len__():
                raise Exception('Number of keys != Number of args in tuple')

            iters = dict((x, y) for x, y in self.__dict__.items() if x[:2] != '__')
            iters.update(self.__dict__)
            counter: int = 0
            for key, value in iters.items():
                if key != '_DbModel__fillMenu':
                    newVal = serverResponse[counter]
                    if isinstance(newVal, int) or str(newVal).isdigit():
                        newVal = str(newVal)
                    if value['type'] == 'money':
                        newVal = str(int(re.search(r'\d+', newVal).group()))
                    if isinstance(newVal, datetime.date):
                        newVal = newVal.strftime('%Y-%m-%d')

                    self.__fillValue(key, value['type'], newVal)
                    counter += 1
        except Exception as err:
            print('Error in parse method! ', err)

    def isFull(self):
        for value in self.__dict__.values():
            if not isinstance(value, dict):
                if value is None: return False
            else:
                if value.get('not null', True): return False
                if value['not null']:
                    return False
        return True
