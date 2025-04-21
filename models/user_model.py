from sqlalchemy import Column, String, Integer, Date, Float
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String, nullable=False)
    password = Column("password", String, nullable=False)

    def toJSON(self):
        return {"id":self.id,
            "username": self.username,
            "password" : self.password}




