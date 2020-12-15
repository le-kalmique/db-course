from sqlalchemy import Column, Integer, String, Numeric
from db import Base

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    discount = Column(Numeric)

    def __repr__(self):
      return "<User(name='%s'," \
             " email='%s'," \
             " phone_number='%s'," \
             " discount='%i')>" % \
             (self.name,
              self.email,
              self.phone_number,
              self.discount)

    def __init__(self,
                 name: str,
                 email: str,
                 phone_number: str,
                 discount: int):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.discount = discount
