from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def generate_trip_plan (user, trip, past_trips):
    prompt = f"""
    You are a personalized travel planning AI. 
    Based on the user's profile and past trip history, generate a detailed day-by-day itinerary. 
    Return the plan as plain text.
    Plan a trip for the user: 
    User Name: {user.name}
    User Age: {user.age}
    User Location: {user.city}
    User Preferemces: {str(user.preferences)}
    Trip Destination: {trip.destination}
    Trip Budget Amount: {trip.budget_amount}
    Trip Budget Currency: {trip.budget_currency}
    Trip Duration: {trip.duration}
    Trip Multiple Cities: {trip.cities}
    Trip Activities: {trip.activities}
    Trip Group Size: {trip.group_size}
    Trip Transportation: {trip.transportation}
    Trip Notes: {trip.notes}
    Past Trip: {
        [
            f"- {t.destination}: highlights={t.highlights}, pain_points={t.pain_points}, rating={t.rating}" for t in past_trips
        ]
    }          
    """

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def generate_ai_notes(trip):
    prompt = f"""
    Based on this completed trip review, 
    write a short summary of what you learned about 
    this user's travel preferences and style. 
    This will be used to personalize future trip recommendations. 
    User Travel Style: {trip.travel_style}
    Trip Pain Points: {trip.pain_points}
    Trip Highlights: {trip.highlights}
    Trip Rating: {trip.rating}
    """
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content