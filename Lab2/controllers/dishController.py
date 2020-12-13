import time

from models.dish import Dish
from database import connect, cursor

class DishController(object):

    def getAll(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            cursor.execute(
                f'SELECT {Dish().getKeys()} FROM "Dish" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = cursor.fetchall()
            for record in records:
                tmpItem = Dish()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            raise err
        return items

    def add(self, *args):
        try:
            newEntity: Dish = Dish()
            if len(args) > 0 and isinstance(args[0], Dish):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                cursor.execute(f'INSERT INTO "Dish" ({newEntity.getKeys()}) '
                                       f'VALUES ({newEntity.getValues()}) RETURNING id')
                connect.commit()
                return int(cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
            connect.rollback()
            raise err
        return False

    def getById(self, dishId):
        dish = Dish()
        try:
            if isinstance(dishId, int): dishId = str(dishId)
            if not isinstance(dishId, str): raise Exception('Incorrect arguments')
            cursor.execute(f'SELECT {dish.getKeys()} from "Dish" WHERE id = {dishId}')
            record = cursor.fetchone()
            if record is not None:
                dish.parse(record)
            else:
                raise Exception(f'No entry with ID {dishId} found')
        except Exception as err:
            print("Get by id error! ", err)
            raise err
        return dish

    def delete(self, dishId):
        try:
            if isinstance(dishId, int): dishId = str(dishId)
            if not isinstance(dishId, str): raise Exception('Incorrect arguments')
            dish = self.getById(dishId)
            cursor.execute(f'DELETE from "Dish" WHERE id = {dishId}')
            connect.commit()
            return dish
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            dish: Dish = Dish()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                dish.fill()
                dish.id = args[0]
                values = dish.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = dish.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        dish.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Dish):
                dish = args[0]

            if not dish.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = dish.getKeys().split(',')
            values = dish.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            cursor.execute(f'Update "Dish" Set {queryStr[:-2]} Where id = {dish.id}')
            connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            cursor.execute(f'SELECT count(*)  from "Dish"')
            return int(cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)
            raise err

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            cursor.execute(f"INSERT  INTO \"Dish\" (name,description,price,restaurant_id) "
                                   f"SELECT generatestring(15),"
                                   f"generatestring(15),"
                                   f"generateint(2000)::numeric,"
                                   f"getrandomrow('Restaurant')::int "
                                   f"FROM generate_series(1, {entitiesNum})")
            connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
            connect.rollback()
            raise err
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'
