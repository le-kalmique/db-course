import time

from models.restaurant import Restaurant
from database import connect, cursor

class RestaurantController(object):

    def getAll(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            cursor.execute(
                f'SELECT {Restaurant().getKeys()} FROM "Restaurant" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = cursor.fetchall()
            for record in records:
                tmpItem = Restaurant()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            raise err
        return items

    def add(self, *args):
        try:
            newEntity: Restaurant = Restaurant()
            if len(args) > 0 and isinstance(args[0], Restaurant):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                cursor.execute(f'INSERT INTO "Restaurant" ({newEntity.getKeys()}) '
                                       f'VALUES ({newEntity.getValues()}) RETURNING id')
                connect.commit()
                return int(cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
            connect.rollback()
            raise err
        return False

    def getById(self, restaurantId):
        restaurant = Restaurant()
        try:
            if isinstance(restaurantId, int): restaurantId = str(restaurantId)
            if not isinstance(restaurantId, str): raise Exception('Incorrect arguments')
            cursor.execute(f'SELECT {restaurant.getKeys()} from "Restaurant" WHERE id = {restaurantId}')
            record = cursor.fetchone()
            if record is not None:
                restaurant.parse(record)
            else:
                raise Exception(f'No entry with ID {restaurantId} found')
        except Exception as err:
            print("Get by id error! ", err)
            raise err
        return restaurant

    def delete(self, restaurantId):
        try:
            if isinstance(restaurantId, int): restaurantId = str(restaurantId)
            if not isinstance(restaurantId, str): raise Exception('Incorrect arguments')
            restaurant = self.getById(restaurantId)
            cursor.execute(f'DELETE from "Restaurant" WHERE id = {restaurantId}')
            connect.commit()
            return restaurant
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            restaurant: Restaurant = Restaurant()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                restaurant.fill()
                restaurant.id = args[0]
                values = restaurant.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = restaurant.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        restaurant.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Restaurant):
                restaurant = args[0]

            if not restaurant.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = restaurant.getKeys().split(',')
            values = restaurant.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            cursor.execute(f'Update "Restaurant" Set {queryStr[:-2]} Where id = {restaurant.id}')
            connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            cursor.execute(f'SELECT count(*)  from "Restaurant"')
            return int(cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)
            raise err

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            cursor.execute(f"INSERT  INTO \"Restaurant\" (name,description,address) "
                                   f"SELECT generatestring(15),"
                                   f"generatestring(50),"
                                   f"generatestring(20) "
                                   f"FROM generate_series(1, {entitiesNum})")
            connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
            connect.rollback()
            raise err
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'
