import time

from models.order import Order
from database import connect, cursor

class OrderController(object):

    def getAll(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            cursor.execute(
                f'SELECT {Order().getKeys()} FROM "Order" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = cursor.fetchall()
            for record in records:
                tmpItem = Order()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            raise err
        return items

    def add(self, *args):
        try:
            newEntity: Order = Order()
            if len(args) > 0 and isinstance(args[0], Order):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                cursor.execute(f'INSERT INTO "Order" ({newEntity.getKeys()}) '
                                       f'VALUES ({newEntity.getValues()}) RETURNING id')
                connect.commit()
                return int(cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
            connect.rollback()
            raise err
        return False

    def getById(self, orderId):
        order = Order()
        try:
            if isinstance(orderId, int): orderId = str(orderId)
            if not isinstance(orderId, str): raise Exception('Incorrect arguments')
            cursor.execute(f'SELECT {order.getKeys()} from "Order" WHERE id = {orderId}')
            record = cursor.fetchone()
            if record is not None:
                order.parse(record)
            else:
                raise Exception(f'No entry with ID {orderId} found')
        except Exception as err:
            print("Get by id error! ", err)
            raise err
        return order

    def delete(self, orderId):
        try:
            if isinstance(orderId, int): orderId = str(orderId)
            if not isinstance(orderId, str): raise Exception('Incorrect arguments')
            order = self.getById(orderId)
            cursor.execute(f'DELETE from "Order" WHERE id = {orderId}')
            connect.commit()
            return order
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            order: Order = Order()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                order.fill()
                order.id = args[0]
                values = order.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = order.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        order.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Order):
                order = args[0]

            if not order.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = order.getKeys().split(',')
            values = order.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            cursor.execute(f'Update "Order" Set {queryStr[:-2]} Where id = {order.id}')
            connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            cursor.execute(f'SELECT count(*)  from "Order"')
            return int(cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)
            raise err

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            cursor.execute(f"INSERT  INTO \"Order\" (user_id,deliverymen_id) "
                                   f"SELECT getrandomrow('User')::int,"
                                   f"getrandomrow('Deliverymen')::int "
                                   f"FROM generate_series(1, {entitiesNum})")
            connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
            connect.rollback()
            raise err
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'
