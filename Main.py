# main.py - UPGRADED FOR LIVE DATABASE
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from supabase import create_client, Client

app = FastAPI()

# --- CORS Configuration ---
origins = ["*"] # Allowing all origins for hackathon simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Supabase Client Initialization ---
# This uses the Environment Variables you set up in Vercel.
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Pydantic Models for Data Validation ---
class LostDogData(BaseModel):
    dog_name: str
    age: str
    breed: str
    size: str
    color: str
    special_markings: Optional[str] = None
    microchip_id: Optional[str] = None
    last_seen_location: str
    contact_phone: str
    photos: List[str]

class SightingData(BaseModel):
    location_sighted: str
    time_sighted: str
    size: str
    behavior: str
    behavior_notes: Optional[str] = None
    photo: str

# --- AI LOGIC ---
def calculate_match_score(lost_dog: dict, new_sighting: SightingData) -> int:
    # This function remains the same, as its logic is sound.
    total_score = 0
    if lost_dog.get('photos') and new_sighting.photo: total_score += 45
    if lost_dog.get('size') == new_sighting.size: total_score += 20
    # ... etc. for all rules.
    return total_score

def handle_new_sighting_logic(sighting_data: SightingData):
    """Fetches active dogs from the LIVE database and runs the matching algorithm."""
    print("AI Matching Triggered for new sighting...")
    try:
        # **UPGRADED CODE:** Fetch from the live Supabase database
        response = supabase.table("lost_dog_profile").select("*").eq("status", "active").execute()
        active_dogs = response.data

        for dog in active_dogs:
            score = calculate_match_score(dog, sighting_data)
            if score >= 40:
                print(f"High-score match found for dog ID {dog['id']} with score {score}!")
    except Exception as e:
        print(f"Error during AI matching: {e}")

# --- API Endpoints ---
@app.post("/api/lost_dog_alert")
async def create_lost_dog_alert(data: LostDogData):
    """Receives new lost dog data and INSERTS it into the live Supabase database."""
    try:
        # **UPGRADED CODE:** This now inserts into your actual Supabase table.
        response = supabase.table("lost_dog_profile").insert(data.dict()).execute()
        return {"message": "Lost dog alert created successfully in live database!", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sighting_report")
async def create_sighting_report(data: SightingData):
    """Receives new sighting data, INSERTS it, and triggers the AI logic."""
    try:
        # **UPGRADED CODE:** This now inserts into your actual Supabase table.
        response = supabase.table("sighting_report").insert(data.dict()).execute()
        
        # Trigger the AI logic to run against the live database
        handle_new_sighting_logic(data)
        
        return {"message": "Sighting report submitted successfully to live database!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
