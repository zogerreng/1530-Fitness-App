from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)

    def toJSON(self):
        return {"id":self.id,
            "email": self.email,
            "password" : self.password}


