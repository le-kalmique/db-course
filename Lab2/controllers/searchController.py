from database import cursor, connect

class SearchController(object):

    def getOrdersByNames(self, deliverymenName: str, userName: str):
        try:
            cursor.execute(
                f'SELECT O.id, array_agg(D.name), array_agg(U.name) from "Order" O ' 
                f'INNER JOIN "Deliverymen" D on D.id = O.deliverymen_id '
                f'INNER JOIN "User" U on U.id = O.user_id '
                f'where D.name like \'{deliverymenName}%\' and U.name like \'{userName}%\' '
                f'group by O.id')
            return cursor.fetchall()
        except Exception as err:
            print("Get error! ", err)
            raise err

    def getUserDishes(self, userName: str):
        try:
            cursor.execute(
                f'Select U.name, array_agg(D.name) from "Link_Dish-Order" links '
                f'INNER JOIN "Dish" D on D.id = links.dish_id '
                f'INNER JOIN "Order" O on O.id = links.order_id ' 
                f'Inner Join "User" U on U.id = O.user_id '
                f'where U.name like \'{userName}%\' '
                f'group by U.name')
            return cursor.fetchall()
        except Exception as err:
            raise str(err)

    def getRestaurantsDeliverymensByRating(self, min: int, max: int, res_name: str):
        try:
            cursor.execute(
                f'Select R.name, array_agg(D2.name) from "Link_Dish-Order" '
                f'INNER JOIN "Dish" D on D.id = "Link_Dish-Order".dish_id '
                f'INNER JOIN "Restaurant" R on R.id = D.restaurant_id '
                f'Inner Join "Order" O on O.id = "Link_Dish-Order".order_id '
                f'Inner Join "Deliverymen" D2 on D2.id = O.deliverymen_id '
                f'where D2.rating > {min} and D2.rating < {max} and R.name like \'%{res_name}%\' '
                f'group by R.name')
            return cursor.fetchall()
        except Exception as err:
            raise str(err)