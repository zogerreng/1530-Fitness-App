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
    
class Food(Base): 
    __tablename__ = 'Foods'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False) 
    calories_per_serving = Column(Float) 
    protein_per_serving = Column(Float) # in grams
    fat_per_serving = Column(Float) # in grams
    serving_size = Column(String)  # in ounces



class Meal(Base):
    __tablename__ = 'Meals'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    date = date = Column(Date, default=datetime.date.today)
    meal_type = Column(String) # breakast, lunch, dinner, snack
    calories = Column(Float) 




