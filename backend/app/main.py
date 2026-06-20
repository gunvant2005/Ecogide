from datetime import date

from flask import Flask, jsonify, request
from flask_cors import CORS

from app.models import ActivityLog, UserProfile
from app.services.assistant_engine import process_message
from app.services.carbon_calculator import calculate_activity_emissions, summarize_footprint
from app.services.insights_engine import generate_insights, generate_recommendations
from app.services import storage

app = Flask(__name__)

# Configure CORS for both local development and Vercel production
# In production on Vercel, frontend and API are served from same domain
# so CORS is not strictly needed, but we keep it for flexibility
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
    "http://localhost:4173",
    # Allow Vercel deployments
    "https://*.vercel.app",
    "*"  # Allow all origins in production
]
CORS(app, origins=cors_origins)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/profile")
def get_profile():
    return jsonify(storage.load_profile().to_dict())


@app.put("/api/profile")
def update_profile():
    data = request.get_json(force=True)
    profile = UserProfile.from_dict(data)
    return jsonify(storage.save_profile(profile).to_dict())


@app.get("/api/activities")
def list_activities():
    days = request.args.get("days", 30, type=int)
    activities = storage.load_activities(days=days)
    result = []
    for a in activities:
        item = a.to_dict()
        item["emissions_kg"] = calculate_activity_emissions(a)
        result.append(item)
    return jsonify(result)


@app.post("/api/activities")
def create_activity():
    data = request.get_json(force=True)
    activity = ActivityLog.from_dict(data)
    if activity.quantity <= 0:
        return jsonify({"error": "Quantity must be positive"}), 400
    saved = storage.add_activity(activity)
    result = saved.to_dict()
    result["emissions_kg"] = calculate_activity_emissions(saved)
    return jsonify(result), 201


@app.delete("/api/activities/<activity_id>")
def remove_activity(activity_id: str):
    if not storage.delete_activity(activity_id):
        return jsonify({"error": "Activity not found"}), 404
    return jsonify({"deleted": True})


@app.get("/api/footprint/summary")
def footprint_summary():
    days = request.args.get("days", 7, type=int)
    profile = storage.load_profile()
    activities = storage.load_activities(days=days)
    return jsonify(summarize_footprint(activities, days=days, weekly_goal=profile.weekly_goal_kg).to_dict())


@app.get("/api/insights")
def insights():
    profile = storage.load_profile()
    activities = storage.load_activities(days=7)
    return jsonify([i.to_dict() for i in generate_insights(activities, profile)])


@app.get("/api/recommendations")
def recommendations():
    profile = storage.load_profile()
    activities = storage.load_activities(days=7)
    return jsonify([r.to_dict() for r in generate_recommendations(activities, profile)])


@app.post("/api/assistant/chat")
def assistant_chat():
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    if not message or len(message) > 500:
        return jsonify({"error": "Message required (max 500 chars)"}), 400
    profile = storage.load_profile()
    activities = storage.load_activities(days=7)
    return jsonify(process_message(message, profile, activities).to_dict())


@app.post("/api/demo/seed")
def seed_demo_data():
    profile = UserProfile(
        name="Alex",
        household_size=1,
        primary_transport="car_petrol",
        diet_type="chicken",
        weekly_goal_kg=80.0,
        home_type="apartment",
    )
    storage.save_profile(profile)
    storage.save_activities([])

    samples = [
        ActivityLog(category="transport", sub_type="car_petrol", quantity=12, unit="km", date=date.today()),
        ActivityLog(category="transport", sub_type="train", quantity=8, unit="km", date=date.today()),
        ActivityLog(category="food", sub_type="chicken", quantity=1, unit="meal", date=date.today()),
        ActivityLog(category="food", sub_type="beef", quantity=1, unit="meal", date=date.today()),
        ActivityLog(category="energy", sub_type="electricity_kwh", quantity=5, unit="kWh", date=date.today()),
        ActivityLog(category="shopping", sub_type="groceries_bag", quantity=1, unit="bag", date=date.today()),
    ]
    for s in samples:
        storage.add_activity(s)

    return jsonify({"seeded": True, "activities": len(samples)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
