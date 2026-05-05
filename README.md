# AI Travel Planner API

## What it is
This as the name says a AI Travel Planner API that personalizes your trips the more you plan
## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- OpenAI API
- Python 3.12.3
## Features
- CRUD for Users and Trips
## How to run locally
1. Clone the repo
2. Create a virtual environment: python3 -m venv venv
3. Activate it: source venv/bin/activate
4. Install dependencies: pip install -r requirements.txt
5. Add your .env file with OPENAI_API_KEY
6. Run: uvicorn main:app --reload
7. Go to http://localhost:8000/docs
## API Endpoints
POST /users/create - creates a new user account
GET /users/{user_id} - gets a user
PUT /users/{user_id} - updates the user's account information  
DELETE /users/{user_id} - deletes the user account information 
POST /users/{user_id}/trips - creates the trips for the user
GET /users/{user_id}/trips - gets all the user's trips
PUT /users/{user_id}/trips/{trip_id} - updates the user's trips
DELETE /users/{user_id}/trips/{trip_id} - deletes the trip information of a singular trips
DELETE /users/{user_id}/trips - deletes all trips for the user
## Roadmap
Trip review endpoint -> AI memory layer that improves with each trip -> Authentication -> Frontend -> Amadeus API for real flight/hotel data
