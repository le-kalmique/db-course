import time

from models.user import User
from database import connect, cursor

class UserController(object):

    def getAll(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            cursor.execute(
                f'SELECT {User().getKeys()} FROM "User" ORDER BY id LIMIT {per_page} OFFSET {page * per_page}')
            records = cursor.fetchall()
            for record in records:
                tmpItem = User()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            raise err
        return items

    def add(self, *args):
        try:
            newEntity: User = User()
            if len(args) > 0 and isinstance(args[0], User):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                cursor.execute(f'INSERT INTO "User" ({newEntity.getKeys()}) '
                                       f'VALUES ({newEntity.getValues()}) RETURNING id')
                connect.commit()
                return int(cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
            connect.rollback()
            raise err
        return False

    def getById(self, userId):
        user = User()
        try:
            if isinstance(userId, int): userId = str(userId)
            if not isinstance(userId, str): raise Exception('Incorrect arguments')
            cursor.execute(f'SELECT {user.getKeys()} from "User" WHERE id = {userId}')
            record = cursor.fetchone()
            if record is not None:
                user.parse(record)
            else:
                raise Exception(f'No entry with ID {userId} found')
        except Exception as err:
            print("Get by id error! ", err)
            raise err
        return user

    def delete(self, userId):
        try:
            if isinstance(userId, int): userId = str(userId)
            if not isinstance(userId, str): raise Exception('Incorrect arguments')
            user = self.getById(userId)
            cursor.execute(f'DELETE from "User" WHERE id = {userId}')
            connect.commit()
            return user
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            user: User = User()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                user.fill()
                user.id = args[0]
                values = user.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = user.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        user.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], User):
                user = args[0]

            if not user.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = user.getKeys().split(',')
            values = user.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            cursor.execute(f'Update "User" Set {queryStr[:-2]} Where id = {user.id}')
            connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            cursor.execute(f'SELECT count(*)  from "User"')
            return int(cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)
            raise err

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            cursor.execute(f"INSERT  INTO \"User\" (name,email,phone_number,discount) "
                                   f"SELECT generatestring(15),"
                                   f"concat(generatestring(15), '@', generatestring(3), '.', generatestring(3)),"
                                   f"concat(generateint(999)::text, '-', generateint(999)::text, '-', generateint(9999)::text),"
                                   f"generateint(100)::numeric "
                                   f"FROM generate_series(1, {entitiesNum})")
            connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
            connect.rollback()
            raise err
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'
