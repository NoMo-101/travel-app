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
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user:
        existing_user.name = user.name
        existing_user.age = user.age
        existing_user.city = user.city
        existing_user.email = user.email
        existing_user.preferences = str(user.preferences)
        db.commit()
        db.refresh(existing_user)
        return {
            'id': existing_user.id,
            'name': existing_user.name,
            'message': f"User {existing_user.name} updated successfully!"      
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user:
        db.delete(existing_user)
        db.commit()
        return{
            'message': f"User account has been deleted"
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")