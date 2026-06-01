from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    city = Column(String)
    email = Column(String, unique=True, index=True)
    preferences = Column(String)  # Store as JSON string for simplicity
    password = Column(String)

class Trip(Base):
    __tablename__ = 'trips'

    #Trip Information
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    destination = Column(String)
    budget_amount = Column(Float)
    budget_currency = Column(String)
    duration = Column(Integer)
    cities = Column(String)
    activities = Column(String)
    group_size = Column(Integer)
    travelers = Column(String)
    transportation = Column(String)
    notes = Column(String)
    status = Column(String, default="planned")
    # AI Memory Layer
    travel_style = Column(String)
    pain_points = Column(String)
    highlights = Column(String)
    rating = Column(Float)
    ai_notes = Column(String)
    #Metadata
    created_at = Column(DateTime, default=datetime.now)
