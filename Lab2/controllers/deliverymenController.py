import time

from models.deliverymen import Deliverymen
from database import connect, cursor

class DeliverymenController(object):

    def getAll(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            cursor.execute(
                f'SELECT {Deliverymen().getKeys()} FROM "Deliverymen" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = cursor.fetchall()
            for record in records:
                tmpItem = Deliverymen()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            connect.rollback()
            raise err
        return items

    def add(self, *args):
        try:
            newEntity: Deliverymen = Deliverymen()
            if len(args) > 0 and isinstance(args[0], Deliverymen):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                cursor.execute(f'INSERT INTO "Deliverymen" ({newEntity.getKeys()}) '
                                       f'VALUES ({newEntity.getValues()}) RETURNING id')
                connect.commit()
                return int(cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
            connect.rollback()
            raise err
        return False

    def getById(self, deliverymenId):
        deliverymen = Deliverymen()
        try:
            if isinstance(deliverymenId, int): deliverymenId = str(deliverymenId)
            if not isinstance(deliverymenId, str): raise Exception('Incorrect arguments')
            cursor.execute(f'SELECT {deliverymen.getKeys()} from "Deliverymen" WHERE id = {deliverymenId}')
            record = cursor.fetchone()
            if record is not None:
                deliverymen.parse(record)
            else:
                raise Exception(f'No entry with ID {deliverymenId} found')
        except Exception as err:
            print("Get by id error! ", err)
            connect.rollback()
            raise err
        return deliverymen

    def delete(self, deliverymenId):
        try:
            if isinstance(deliverymenId, int): deliverymenId = str(deliverymenId)
            if not isinstance(deliverymenId, str): raise Exception('Incorrect arguments')
            deliverymen = self.getById(deliverymenId)
            cursor.execute(f'DELETE from "Deliverymen" WHERE id = {deliverymenId}')
            connect.commit()
            return deliverymen
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            deliverymen: Deliverymen = Deliverymen()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                deliverymen.fill()
                deliverymen.id = args[0]
                values = deliverymen.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = deliverymen.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        deliverymen.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Deliverymen):
                deliverymen = args[0]

            if not deliverymen.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = deliverymen.getKeys().split(',')
            values = deliverymen.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            cursor.execute(f'Update "Deliverymen" Set {queryStr[:-2]} Where id = {deliverymen.id}')
            connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            cursor.execute(f'SELECT count(*)  from "Deliverymen"')
            return int(cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)
            connect.rollback()
            raise err

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            cursor.execute(f"INSERT  INTO \"Deliverymen\" (name,surname,rating) "
                                   f"SELECT generatestring(15),"
                                   f"generatestring(15),"
                                   f"generateint(10)::numeric "
                                   f"FROM generate_series(1, {entitiesNum})")
            connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
            connect.rollback()
            raise err
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'
