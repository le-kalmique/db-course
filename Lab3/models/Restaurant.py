from sqlalchemy import Column, Integer, String
from db import Base


class Restaurant(Base):
    __tablename__ = 'Restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)

    def __repr__(self):
        return "<Restaurant(name='%s'," \
               " description='%s'," \
               " address='%s')>" % \
               (self.name,
                self.description,
                self.address)

    def __init__(self,
                 name: str,
                 description: str,
                 address: str):
        self.name = name
        self.description = description
        self.address = address
