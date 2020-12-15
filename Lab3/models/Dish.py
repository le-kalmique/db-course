from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship, backref
from db import Base
from models.links import link_dish_order

class Dish(Base):
    __tablename__ = 'Dish'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Numeric)
    restaurant_id = Column(Integer, ForeignKey('Restaurant.id', ondelete='CASCADE'))

    Orders = relationship("Order", secondary=link_dish_order, cascade="all,delete")
    Restaurant = relationship("Restaurant", backref=backref("Dish", uselist=False, cascade="all,delete"))

    def __repr__(self):
      return "<Dish(name='%s'," \
             " description='%s'," \
             " price='%i'," \
             "restaurant_id='%i')>" % \
             (self.name,
              self.description,
              self.price,
              self.restaurant_id)

    def __init__(self,
                 name: str,
                 description: str,
                 price: int,
                 restaurant_id: int):
        self.name = name
        self.description = description
        self.price = price
        self.restaurant_id = restaurant_id

