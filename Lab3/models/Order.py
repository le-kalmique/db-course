from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from db import Base


class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'))
    deliverymen_id = Column(Integer, ForeignKey('Deliverymen.id', ondelete='CASCADE'))
    User = relationship("User", backref=backref("Order", uselist=False, cascade="all,delete"))
    Deliverymen = relationship("Deliverymen", backref=backref("Order", uselist=False, cascade="all,delete"))

    def __repr__(self):
      return "<Order(user_id='%i', deliverymen_id='%i')>" % \
             (self.user_id, self.deliverymen_id)

    def __init__(self, user_id: int, deliverymen_id: int):
        self.user_id = user_id
        self.deliverymen_id = deliverymen_id

