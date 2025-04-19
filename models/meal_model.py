from sqlalchemy import Table, Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

meal_food_table = Table(
    'meal_food',
    Base.metadata,
    Column('meal_id', Integer, ForeignKey('Meals.id'), primary_key=True),
    Column('food_id', Integer, ForeignKey('Foods.id'), primary_key=True)
)

class Meal(Base):
    __tablename__ = 'Meals'

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    date = date = Column(Date, default=datetime.date.today)
    meal_type = Column(String) # breakast, lunch, dinner, snack
    calories = Column(Float)

    foods = relationship('Food', secondary=meal_food_table, back_populates='Meals')

class Food(Base): 
    __tablename__ = 'Foods'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False) 
    calories_per_serving = Column(Float) 
    protein_per_serving = Column(Float) # in grams
    fat_per_serving = Column(Float) # in grams
    serving_size = Column(String)  # in ounces

    meals = relationship('Meal', secondary=meal_food_table, back_populates='Foods')


