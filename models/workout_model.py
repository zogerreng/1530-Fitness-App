from sqlalchemy import Table, Column, String, Integer, Date, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

Base = declarative_base()

# Association table for many-to-many relationship
workout_exercise_table = Table(
    'workout_exercise',
    Base.metadata,
    Column('workout_id', Integer, ForeignKey('Workouts.id'), primary_key=True),
    Column('exercise_id', Integer, ForeignKey('Exercises.id'), primary_key=True)
)

class Workout(Base):
    __tablename__ = 'Workouts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, default=datetime.date.today)

    exercises = relationship('Exercise', secondary=workout_exercise_table, back_populates='workouts')

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "exercises": [exercise.to_dict() for exercise in self.exercises]
        }

class Exercise(Base):
    __tablename__ = 'Exercises'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    repetitions = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    intensity = Column(String, nullable=False)

    workouts = relationship('Workout', secondary=workout_exercise_table, back_populates='exercises')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "repetitions": self.repetitions,
            "weight": self.weight,
            "intensity": self.intensity
        }

# Example engine and session creation
# engine = create_engine('sqlite:///workouts.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
