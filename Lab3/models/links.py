from sqlalchemy import Column, Integer, Table, ForeignKey
from db import Base

link_dish_order = Table(
    'Link_Dish-Order', Base.metadata,
    Column('dish_id', Integer, ForeignKey('Dish.id')),
    Column('order_id', Integer, ForeignKey('Order.id'))
)



