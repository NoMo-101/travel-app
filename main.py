from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class TripRequest(BaseModel):
    destination: str
    days: int
    budget: str

class UserProfile(BaseModel):
    name: str
    age: int
    city: str
    email: Optional[str] = None
    preferences: dict

@app.get("/")
def root():
    return {"message": "Trip Planner API is alive 🌍"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/trips/plan")
def plan_trip(trip: TripRequest):
    return {
        "destination": trip.destination,
        "days": trip.days,
        "budget": trip.budget,
        "message": f"Planning your {trip.days} day trip to {trip.destination}!"
    }

@app.post("/users/create")
def create_user(user: UserProfile):
    return {
        "name": user.name,
        "age": user.age,
        "city": user.city,
        "email": user.email,
        "preferences": user.preferences,
        "message": f"User {user.name} created account successfully!"
    }