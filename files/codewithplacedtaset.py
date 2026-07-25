from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from google import genai


load_dotenv()

print("KEY:", os.environ.get("GOOGLE_API_KEY"))

client = genai.Client(
    api_key=os.environ.get("GOOGLE_API_KEY")
)

app = Flask(__name__)

# ─── PLACES DATABASE ───────────────────────────────────────────────────────────
PLACES = [
    {
        "id": 1,
        "name": "Murree",
        "city": "Punjab",
        "type": "mountain",
        "temp": "cool",
        "crowd": "medium",
        "budget": "medium",
        "mood": ["relax", "explore", "romantic"],
        "description": "A classic hill station with pine forests, cool breeze, and scenic viewpoints.",
        "best_time": "March – October",
        "activities": ["hiking", "sightseeing", "shopping"],
        "image_icon": "mountain"
    },
    {
        "id": 2,
        "name": "Nathia Gali",
        "city": "KPK",
        "type": "mountain",
        "temp": "cool",
        "crowd": "low",
        "budget": "medium",
        "mood": ["relax", "explore", "solo"],
        "description": "Serene hill town with dense forests and peaceful trails away from the crowds.",
        "best_time": "April – September",
        "activities": ["hiking", "nature walks", "bird watching"],
        "image_icon": "mountain"
    },
    {
        "id": 3,
        "name": "Clifton Beach",
        "city": "Karachi",
        "type": "beach",
        "temp": "warm",
        "crowd": "high",
        "budget": "low",
        "mood": ["social", "fun", "family"],
        "description": "Karachi's iconic beach with street food, camel rides, and a lively atmosphere.",
        "best_time": "November – February",
        "activities": ["swimming", "street food", "camel riding"],
        "image_icon": "beach"
    },
    {
        "id": 4,
        "name": "French Beach",
        "city": "Karachi",
        "type": "beach",
        "temp": "warm",
        "crowd": "low",
        "budget": "medium",
        "mood": ["relax", "romantic", "solo"],
        "description": "A quiet, pristine beach outside Karachi perfect for peaceful getaways.",
        "best_time": "October – March",
        "activities": ["swimming", "snorkeling", "camping"],
        "image_icon": "beach"
    },
    {
        "id": 5,
        "name": "Lahore Gulshan-e-Iqbal Park",
        "city": "Lahore",
        "type": "park",
        "temp": "mild",
        "crowd": "medium",
        "budget": "low",
        "mood": ["family", "relax", "social"],
        "description": "A large urban park with lakes, jogging tracks, and recreational areas.",
        "best_time": "October – March",
        "activities": ["jogging", "picnic", "boating"],
        "image_icon": "park"
    },
    {
        "id": 6,
        "name": "Fatima Jinnah Park",
        "city": "Islamabad",
        "type": "park",
        "temp": "mild",
        "crowd": "low",
        "budget": "low",
        "mood": ["relax", "solo", "family"],
        "description": "A peaceful, well-maintained green park in the heart of Islamabad.",
        "best_time": "Year-round",
        "activities": ["jogging", "cycling", "picnic"],
        "image_icon": "park"
    },
    {
        "id": 7,
        "name": "Gloria Jeans Gulberg",
        "city": "Lahore",
        "type": "indoor",
        "temp": "cool",
        "crowd": "medium",
        "budget": "high",
        "mood": ["social", "focus", "romantic"],
        "description": "A cozy, upscale café with great ambience for work or casual meetups.",
        "best_time": "Year-round",
        "activities": ["coffee", "work", "meetings"],
        "image_icon": "cafe"
    },
    {
        "id": 8,
        "name": "Burning Brownie Café",
        "city": "Karachi",
        "type": "indoor",
        "temp": "cool",
        "crowd": "medium",
        "budget": "medium",
        "mood": ["social", "focus", "romantic"],
        "description": "Trendy café with warm lighting, great desserts, and a relaxed indoor vibe.",
        "best_time": "Year-round",
        "activities": ["coffee", "desserts", "study"],
        "image_icon": "cafe"
    },
    {
        "id": 9,
        "name": "Hunza Valley",
        "city": "Gilgit-Baltistan",
        "type": "mountain",
        "temp": "cool",
        "crowd": "low",
        "budget": "high",
        "mood": ["explore", "romantic", "adventure"],
        "description": "One of Pakistan's most breathtaking valleys with dramatic peaks and cherry blossoms.",
        "best_time": "April – October",
        "activities": ["trekking", "sightseeing", "photography"],
        "image_icon": "mountain"
    },
    {
        "id": 10,
        "name": "Keenjhar Lake",
        "city": "Sindh",
        "type": "park",
        "temp": "mild",
        "crowd": "medium",
        "budget": "low",
        "mood": ["relax", "family", "social"],
        "description": "Pakistan's second largest freshwater lake, perfect for boating and picnics.",
        "best_time": "October – February",
        "activities": ["boating", "fishing", "picnic"],
        "image_icon": "lake"
    },
    {
        "id": 11,
        "name": "Swat Valley",
        "city": "KPK",
        "type": "mountain",
        "temp": "cool",
        "crowd": "medium",
        "budget": "medium",
        "mood": ["explore", "family", "adventure"],
        "description": "The Switzerland of Pakistan — lush green meadows, rivers, and snow-capped peaks.",
        "best_time": "April – September",
        "activities": ["rafting", "hiking", "sightseeing"],
        "image_icon": "mountain"
    },
    {
        "id": 12,
        "name": "Hawksbay Beach",
        "city": "Karachi",
        "type": "beach",
        "temp": "warm",
        "crowd": "low",
        "budget": "low",
        "mood": ["relax", "family", "solo"],
        "description": "A calm, quieter beach near Karachi great for relaxing away from the busy city.",
        "best_time": "November – February",
        "activities": ["swimming", "sunbathing", "camping"],
        "image_icon": "beach"
    },
    {
        "id": 13,
        "name": "Coworking Café F-7",
        "city": "Islamabad",
        "type": "indoor",
        "temp": "cool",
        "crowd": "low",
        "budget": "medium",
        "mood": ["focus", "solo", "work"],
        "description": "A quiet, well-equipped indoor space ideal for focused work and productivity.",
        "best_time": "Year-round",
        "activities": ["work", "study", "coffee"],
        "image_icon": "cafe"
    },
    {
        "id": 14,
        "name": "Saiful Muluk Lake",
        "city": "KPK",
        "type": "mountain",
        "temp": "cool",
        "crowd": "medium",
        "budget": "high",
        "mood": ["explore", "romantic", "adventure"],
        "description": "A legendary glacial lake at 3,200m surrounded by towering peaks — truly magical.",
        "best_time": "June – September",
        "activities": ["trekking", "photography", "sightseeing"],
        "image_icon": "mountain"
    },
    {
        "id": 15,
        "name": "DHA Phase 8 Park",
        "city": "Karachi",
        "type": "park",
        "temp": "mild",
        "crowd": "low",
        "budget": "low",
        "mood": ["relax", "solo", "focus"],
        "description": "A well-maintained neighbourhood park, quiet and perfect for a peaceful morning.",
        "best_time": "Year-round",
        "activities": ["jogging", "meditation", "reading"],
        "image_icon": "park"
    },
]

# ─── SCORING ALGORITHM ─────────────────────────────────────────────────────────
def calculate_match(user_prefs, place):
    score = 0
    breakdown = {}

    # Location type match (25 pts)
    if user_prefs.get("location_type") == place["type"]:
        score += 25
        breakdown["location"] = 25
    else:
        breakdown["location"] = 0

    # Temperature match (20 pts)
    if user_prefs.get("temperature") == place["temp"]:
        score += 20
        breakdown["temperature"] = 20
    else:
        breakdown["temperature"] = 0

    # Crowd match (20 pts)
    if user_prefs.get("crowd") == place["crowd"]:
        score += 20
        breakdown["crowd"] = 20
    elif abs(["low","medium","high"].index(user_prefs.get("crowd","medium")) -
             ["low","medium","high"].index(place["crowd"])) == 1:
        score += 10
        breakdown["crowd"] = 10
    else:
        breakdown["crowd"] = 0

    # Budget match (20 pts)
    if user_prefs.get("budget") == place["budget"]:
        score += 20
        breakdown["budget"] = 20
    elif abs(["low","medium","high"].index(user_prefs.get("budget","medium")) -
             ["low","medium","high"].index(place["budget"])) == 1:
        score += 10
        breakdown["budget"] = 10
    else:
        breakdown["budget"] = 0

    # Mood match (15 pts)
    user_mood = user_prefs.get("mood", "")
    if user_mood in place["mood"]:
        score += 15
        breakdown["mood"] = 15
    else:
        breakdown["mood"] = 0

    return score, breakdown


def get_top_matches(user_prefs, top_n=3):
    scored = []
    for place in PLACES:
        score, breakdown = calculate_match(user_prefs, place)
        scored.append({**place, "match_score": score, "breakdown": breakdown})
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:top_n]

#Ai comparison
def ai_compare_places(top_places, user_prefs):
    try:
        print("🔥 AI FUNCTION CALLED")

        api_key = os.environ.get("GOOGLE_API_KEY")
        print("KEY:", api_key)

        if not api_key:
            return "AI comparison unavailable — API key missing."

        client = genai.Client(api_key=api_key)

        # ─── Prepare places summary ─────────────────────────────
        places_summary = "\n".join([
            f"{i+1}. {p['name']} ({p['city']}) — Match: {p['match_score']}% — {p['description']}"
            for i, p in enumerate(top_places)
        ])

        # ─── Prepare user summary ──────────────────────────────
        user_summary = (
            f"Mood: {user_prefs.get('mood')}, "
            f"Location type: {user_prefs.get('location_type')}, "
            f"Temperature: {user_prefs.get('temperature')}, "
            f"Crowd: {user_prefs.get('crowd')}, "
            f"Budget: {user_prefs.get('budget')}"
        )

        # ─── AI Prompt ─────────────────────────────────────────
        prompt = f"""
You are SeasonScape's AI advisor helping a Pakistani user choose the perfect real-world environment.

User Preferences:
{user_summary}

Top Matched Places:
{places_summary}

Compare these places in a friendly and conversational way.
Clearly recommend the BEST option and explain why.
Mention strengths and trade-offs briefly.
Keep response within 4-5 sentences.
"""

        # ─── First Model Attempt ───────────────────────────────
        try:
            print("⚡ Trying primary model: gemini-2.5-flash")

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        # ─── Fallback Model ────────────────────────────────────
        except Exception as primary_error:
            print("❌ Primary model failed:", primary_error)
            print("⚡ Switching to fallback model: gemini-2.0-flash")

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

        print("✅ AI RESPONSE GENERATED")

        return response.text

    except Exception as e:
        print("❌ FINAL ERROR:", e)

        return (
            "AI analysis is temporarily busy right now. "
            "Please try again in a few seconds."
        )

# ─── ROUTES ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/api/match", methods=["POST"])
def match():
    data = request.json
    user_prefs = {
        "mood": data.get("mood"),
        "location_type": data.get("location_type"),
        "temperature": data.get("temperature"),
        "crowd": data.get("crowd"),
        "budget": data.get("budget"),
        "name": data.get("name", "Explorer")
    }

    top_matches = get_top_matches(user_prefs, top_n=3)
    ai_analysis = ai_compare_places(top_matches, user_prefs)

    return jsonify({
        "user_prefs": user_prefs,
        "matches": top_matches,
        "ai_analysis": ai_analysis
    })


if __name__ == "__main__":
    app.run(debug=True)




