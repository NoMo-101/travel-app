from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import SessionLocal, Base, engine
from models import User, Trip



Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TripRequest(BaseModel):
    destination: str
    budget_amount: float
    budget_currency: str
    duration: int
    cities: Optional[str] = None
    activities: Optional[str] = None
    group_size: int
    travelers: Optional[str] = None
    transportation: Optional[str] = None
    notes: Optional[str] = None


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

@app.post("/users/create")
def create_user(user: UserProfile, db: SessionLocal = Depends(get_db)):
    db_user = User(
        name = user.name,
        age = user.age,
        city = user.city,
        email = user.email,
        preferences = str(user.preferences)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        'id': db_user.id,
        'name': db_user.name,
        'message': f"User {db_user.name} created successfully!"      
    }

@app.get("/users/{user_id}")
def get_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return {
            'id': user.id,
            'name': user.name,
            'age': user.age,
            'city': user.city,
            'email': user.email,
            'preferences': user.preferences
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{update}")
def update_user(user_id: int, user: UserProfile, db: SessionLocal = Depends(get_db)):
    existing_user_update = db.query(User).filter(User.id == user_id).first()
    if existing_user_update:
        existing_user_update.name = user.name
        existing_user_update.age = user.age
        existing_user_update.city = user.city
        existing_user_update.email = user.email
        existing_user_update.preferences = str(user.preferences)
        db.commit()
        db.refresh(existing_user_update)
        return {
            'id': existing_user_update.id,
            'name': existing_user_update.name,
            'message': f"User {existing_user_update.name} updated successfully!"      
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: SessionLocal = Depends(get_db)):
    existing_user_delete = db.query(User).filter(User.id == user_id).first()
    if existing_user_delete:
        db.delete(existing_user_delete)
        db.commit()
        return{
            'message': f"User account has been deleted"
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.post("/users/{user_id}/trips")
def create_trip(trip: TripRequest, user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user_trips = Trip(
            user_id = user_id,
            destination = trip.destination,
            budget_amount = trip.budget_amount,
            budget_currency = trip.budget_currency,
            duration = trip.duration,
            cities = trip.cities,
            activities = trip.activities,
            group_size = trip.group_size,
            travelers = trip.travelers,
            transportation = trip.transportation,
            notes = trip.notes
        )
        db.add(user_trips)
        db.commit()
        db.refresh(user_trips)
        return {
            'id': user_trips.id,
            "destination": trip.destination,
            "budget_amount": trip.budget_amount,
            "budget_currency": trip.budget_currency,
            "duration": trip.duration,
            "cities": trip.cities,
            "activities": trip.activities,
            "group_size": trip.group_size,
            "transportation": trip.transportation,
            "notes": trip.notes,
            "message": f"Planning your {trip.duration} day trip to {trip.destination}!"
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.get("/users/{user_id}/trips")
def get_trips(user_id: int, db: SessionLocal = Depends(get_db)):
    trips = db.query(Trip).filter(Trip.user_id == user_id).all()
    if trips:
        return [
            {
                "id": trip.id,
                "budget_amount": trip.budget_amount,
                "budget_currency": trip.budget_currency,
                "duration": trip.duration,
                "cities": trip.cities,
                "activities": trip.activities,
                "group_size": trip.group_size,
                "transportation": trip.transportation,
                "notes": trip.notes,
                "status": trip.status,
                "created_at": str(trip.created_at)
            }
            for trip in trips
        ]
    else:
        raise HTTPException(status_code=404, detail="No trips found")

@app.put("/users/{user_id}/trips/{trip_id}")
def update_trip(trip: TripRequest, user_id: int, trip_id: int, db: SessionLocal = Depends(get_db)):
    existing_trip_update = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if existing_trip_update:
        existing_trip_update.destination = trip.destination
        existing_trip_update.budget_amount = trip.budget_amount
        existing_trip_update.budget_currency = trip.budget_currency
        existing_trip_update.duration = trip.duration
        existing_trip_update.cities = trip.cities
        existing_trip_update.activities = trip.activities
        existing_trip_update.group_size = trip.group_size
        existing_trip_update.travelers = trip.travelers
        existing_trip_update.transportation = trip.transportation
        existing_trip_update.notes = trip.notes
        db.commit()
        db.refresh(existing_trip_update)
        return{
            "id": existing_trip_update.id,
            "message": f"Trip to {existing_trip_update.destination} has been updated"
        }
    else:
        raise HTTPException(status_code=404, detail="No trips found")



@app.delete("/users/{user_id}/trips/{trip_id}")
def delete_trips(user_id: int, trip_id: int, db: SessionLocal = Depends(get_db)):
    existing_trip_delete = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if existing_trip_delete:
        db.delete(existing_trip_delete)
        db.commit()
        return{
            'message': f"Trip has been deleted"
        }
    else:
        raise HTTPException(status_code=404, detail="Trip not found")