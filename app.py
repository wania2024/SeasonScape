from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from google import genai
import heapq



load_dotenv()


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
        "mood": ["relax", "explore", "nature", "photography"],
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
        "mood": ["relax", "explore", "solo", "nature", "wellness"],
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
        "mood": ["social", "fun", "family", "foodie"],
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
        "mood": ["relax", "solo", "nature", "wellness"],
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
        "mood": ["family", "relax", "social", "fitness", "wellness"],
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
        "mood": ["relax", "solo", "family", "fitness", "wellness"],
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
        "mood": ["social", "focus", "luxury", "foodie", "work"],
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
        "mood": ["social", "focus", "creative", "foodie"],
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
        "mood": ["explore", "adventure", "nature", "photography"],
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
        "mood": ["relax", "family", "social", "nature"],
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
        "mood": ["explore", "family", "adventure", "nature", "photography"],
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
        "mood": ["relax", "family", "solo", "wellness"],
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
        "mood": ["focus", "solo", "work", "creative"],
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
        "mood": ["explore", "adventure", "nature", "photography"],
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
        "mood": ["relax", "solo", "focus", "fitness", "wellness"],
        "description": "A well-maintained neighbourhood park, quiet and perfect for a peaceful morning.",
        "best_time": "Year-round",
        "activities": ["jogging", "meditation", "reading"],
        "image_icon": "park"
    },
    {
        "id": 16,
        "name": "Fairy Meadows",
        "city": "Gilgit-Baltistan",
        "type": "mountain",
        "temp": "cool",
        "crowd": "low",
        "budget": "high",
        "mood": ["adventure", "explore", "solo", "photography"],
        "description": "A breathtaking meadow near Nanga Parbat offering unforgettable camping experiences.",
        "best_time": "May – September",
        "activities": ["camping", "trekking", "photography"],
        "image_icon": "mountain"
    },
    {
        "id": 17,
        "name": "Shogran Valley",
        "city": "KPK",
        "type": "mountain",
        "temp": "cool",
        "crowd": "medium",
        "budget": "medium",
        "mood": ["relax", "family", "explore", "photography"],
        "description": "Beautiful green meadows and peaceful mountain scenery perfect for family trips.",
        "best_time": "April – October",
        "activities": ["horse riding", "hiking", "photography"],
        "image_icon": "mountain"
    },
    {
        "id": 18,
        "name": "Pir Sohawa",
        "city": "Islamabad",
        "type": "mountain",
        "temp": "cool",
        "crowd": "high",
        "budget": "medium",
        "mood": ["social", "relax", "foodie", "nightlife"],
        "description": "A scenic hilltop destination overlooking Islamabad with restaurants and viewpoints.",
        "best_time": "Year-round",
        "activities": ["dining", "sightseeing", "driving"],
        "image_icon": "mountain"
    },
    {
        "id": 19,
        "name": "Kund Malir Beach",
        "city": "Balochistan",
        "type": "beach",
        "temp": "warm",
        "crowd": "low",
        "budget": "medium",
        "mood": ["relax", "adventure", "solo", "photography"],
        "description": "A stunning untouched beach along the Makran Coastal Highway.",
        "best_time": "November – February",
        "activities": ["camping", "photography", "swimming"],
        "image_icon": "beach"
    },
    {
        "id": 20,
        "name": "Sandspit Beach",
        "city": "Karachi",
        "type": "beach",
        "temp": "warm",
        "crowd": "medium",
        "budget": "low",
        "mood": ["family", "social", "fun", "foodie"],
        "description": "A popular sandy beach known for picnics and turtle nesting sites.",
        "best_time": "October – March",
        "activities": ["picnic", "camel riding", "swimming"],
        "image_icon": "beach"
    },
    {
        "id": 21,
        "name": "Bahria Town Eiffel Park",
        "city": "Lahore",
        "type": "park",
        "temp": "mild",
        "crowd": "medium",
        "budget": "low",
        "mood": ["family", "social", "relax", "photography"],
        "description": "A lively park inspired by Paris with fountains and evening lights.",
        "best_time": "October – March",
        "activities": ["walking", "photography", "family picnic"],
        "image_icon": "park"
    },
    {
        "id": 22,
        "name": "Lake View Park",
        "city": "Islamabad",
        "type": "park",
        "temp": "mild",
        "crowd": "medium",
        "budget": "medium",
        "mood": ["family", "social", "fun", "fitness"],
        "description": "A large recreational park near Rawal Lake with boating and attractions.",
        "best_time": "Year-round",
        "activities": ["boating", "picnic", "cycling"],
        "image_icon": "park"
    },
    {
        "id": 23,
        "name": "Second Cup DHA",
        "city": "Lahore",
        "type": "indoor",
        "temp": "cool",
        "crowd": "low",
        "budget": "high",
        "mood": ["focus", "solo", "work", "study"],
        "description": "A peaceful premium café suitable for studying and focused work.",
        "best_time": "Year-round",
        "activities": ["coffee", "study", "meetings"],
        "image_icon": "cafe"
    },
    {
        "id": 24,
        "name": "Chaye Khana",
        "city": "Islamabad",
        "type": "indoor",
        "temp": "cool",
        "crowd": "medium",
        "budget": "medium",
        "mood": ["social", "relax", "foodie", "study"],
        "description": "A warm and cozy café famous for tea, books, and peaceful ambience.",
        "best_time": "Year-round",
        "activities": ["tea", "reading", "conversation"],
        "image_icon": "cafe"
    },
    {
        "id": 25,
        "name": "Malam Jabba",
        "city": "KPK",
        "type": "mountain",
        "temp": "cold",
        "crowd": "medium",
        "budget": "high",
        "mood": ["adventure", "explore", "fun", "photography"],
        "description": "Pakistan’s famous ski resort with snowy slopes and chairlifts.",
        "best_time": "December – February",
        "activities": ["skiing", "snowboarding", "chairlift rides"],
        "image_icon": "mountain"
    },
    {
        "id": 26,
        "name": "Ormara Beach",
        "city": "Balochistan",
        "type": "beach",
        "temp": "warm",
        "crowd": "low",
        "budget": "medium",
        "mood": ["solo", "relax", "photography", "adventure"],
        "description": "A quiet coastal destination with crystal-clear waters and peaceful surroundings.",
        "best_time": "November – February",
        "activities": ["camping", "swimming", "stargazing"],
        "image_icon": "beach"
    },
    {
        "id": 27,
        "name": "Jilani Park",
        "city": "Lahore",
        "type": "park",
        "temp": "mild",
        "crowd": "medium",
        "budget": "low",
        "mood": ["family", "relax", "fitness", "solo"],
        "description": "A famous jogging and family park known for flower exhibitions.",
        "best_time": "October – April",
        "activities": ["jogging", "walking", "picnic"],
        "image_icon": "park"
    },
    {
        "id": 28,
        "name": "Coffee Bean & Tea Leaf",
        "city": "Karachi",
        "type": "indoor",
        "temp": "cool",
        "crowd": "medium",
        "budget": "high",
        "mood": ["focus", "social", "work", "study"],
        "description": "A stylish café chain with a calm atmosphere for meetings and work.",
        "best_time": "Year-round",
        "activities": ["coffee", "work", "study"],
        "image_icon": "cafe"
    },
    {
        "id": 29,
        "name": "Ratti Gali Lake",
        "city": "AJK",
        "type": "mountain",
        "temp": "cool",
        "crowd": "low",
        "budget": "high",
        "mood": ["adventure", "explore", "photography", "solo"],
        "description": "A spectacular alpine lake surrounded by snowy mountains and green valleys.",
        "best_time": "June – September",
        "activities": ["trekking", "camping", "photography"],
        "image_icon": "mountain"
    },
    {
        "id": 30,
        "name": "Port Grand",
        "city": "Karachi",
        "type": "indoor",
        "temp": "mild",
        "crowd": "high",
        "budget": "high",
        "mood": ["social", "family", "fun", "foodie", "nightlife"],
        "description": "A lively food and entertainment destination by the waterfront.",
        "best_time": "Year-round",
        "activities": ["dining", "shopping", "live music"],
        "image_icon": "cafe"
    }
]

# ─── SCORING ALGORITHM ─────────────────────────────────────────────────────────
def calculate_match(user_prefs, place):
    score = 0
    breakdown = {}

    # Location type (HIGH importance)
    if user_prefs.get("location_type") == place["type"]:
        score += 25
        breakdown["location"] = 25
    else:
        breakdown["location"] = 0

    # Temperature
    if user_prefs.get("temperature") == place["temp"]:
        score += 20
        breakdown["temperature"] = 20
    else:
        breakdown["temperature"] = 0

    # Crowd (A* improvement → distance-based penalty)
    crowd_levels = ["low", "medium", "high"]

    user_crowd = crowd_levels.index(user_prefs.get("crowd", "medium"))
    place_crowd = crowd_levels.index(place["crowd"])

    crowd_diff = abs(user_crowd - place_crowd)

    if crowd_diff == 0:
        score += 20
        breakdown["crowd"] = 20
    elif crowd_diff == 1:
        score += 10
        breakdown["crowd"] = 10
    else:
        breakdown["crowd"] = 0

    # Budget (A* style cost function)
    budget_levels = ["low", "medium", "high"]

    user_budget = budget_levels.index(user_prefs.get("budget", "medium"))
    place_budget = budget_levels.index(place["budget"])

    budget_diff = abs(user_budget - place_budget)

    if budget_diff == 0:
        score += 20
        breakdown["budget"] = 20
    elif budget_diff == 1:
        score += 10
        breakdown["budget"] = 10
    else:
        breakdown["budget"] = 0

    # Mood match
    if user_prefs.get("mood") in place["mood"]:
        score += 15
        breakdown["mood"] = 15
    else:
        breakdown["mood"] = 0

    # ─── A* COST FUNCTION (NEW PART) ───
    cost = 100 - score   # lower cost = better match

    return score, breakdown, cost


def get_top_matches(user_prefs, top_n=3):
    priority_queue = []

    for place in PLACES:
        score, breakdown, cost = calculate_match(user_prefs, place)

        enriched_place = {
            **place,
            "match_score": score,
            "breakdown": breakdown,
            "cost": cost
        }

        # A* priority queue
        heapq.heappush(
            priority_queue,
            (cost, place["id"], enriched_place)
        )

    results = []

    for _ in range(min(top_n, len(priority_queue))):
        cost, _, place = heapq.heappop(priority_queue)
        results.append(place)

    return results


#Ai comparison
def ai_compare_places(top_places, user_prefs):
    try:
        print("🔥 AI FUNCTION CALLED")

        api_key = os.environ.get("GOOGLE_API_KEY")
        
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
    app.run(debug=False)
