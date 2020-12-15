from sqlalchemy import Column, Integer, String, Numeric
from db import Base

class Deliverymen(Base):
    __tablename__ = 'Deliverymen'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    rating = Column(Numeric)

    def __repr__(self):
      return "<Deliverymen(name='%s'," \
             " surname='%s'," \
             " rating='%i')>" % \
             (self.name,
              self.surname,
              self.rating)

    def __init__(self,
                 name: str,
                 surname: str,
                 rating: int):
        self.name = name
        self.surname = surname
        self.rating = rating
