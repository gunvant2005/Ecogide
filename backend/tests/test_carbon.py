import pytest
from datetime import date

from app.models import ActivityLog, UserProfile
from app.services.carbon_calculator import calculate_activity_emissions, summarize_footprint
from app.services.assistant_engine import detect_intent, process_message
from app.services.insights_engine import generate_insights, generate_recommendations


def test_transport_emissions():
    activity = ActivityLog(
        category="transport",
        sub_type="car_petrol",
        quantity=10,
        unit="km",
        date=date.today(),
    )
    assert calculate_activity_emissions(activity) == 2.1


def test_bike_zero_emissions():
    activity = ActivityLog(
        category="transport",
        sub_type="bike",
        quantity=20,
        unit="km",
        date=date.today(),
    )
    assert calculate_activity_emissions(activity) == 0.0


def test_food_emissions():
    activity = ActivityLog(
        category="food",
        sub_type="beef",
        quantity=2,
        unit="meal",
        date=date.today(),
    )
    assert calculate_activity_emissions(activity) == 13.0


def test_footprint_summary():
    today = date.today()
    activities = [
        ActivityLog(category="transport", sub_type="train", quantity=10, unit="km", date=today),
        ActivityLog(category="food", sub_type="vegan", quantity=1, unit="meal", date=today),
    ]
    summary = summarize_footprint(activities, days=7, weekly_goal=80)
    assert summary.total_kg == 1.1
    assert summary.by_category["transport"] == 0.4
    assert summary.by_category["food"] == 0.7


def test_intent_detection():
    assert detect_intent("Hello there") == "greeting"
    assert detect_intent("How am I doing this week?") == "footprint_status"
    assert detect_intent("Tips to reduce my footprint") == "reduce_tips"
    assert detect_intent("How do I log a meal?") == "log_help"


def test_assistant_footprint_reply():
    profile = UserProfile(name="Test", weekly_goal_kg=80)
    activities = [
        ActivityLog(category="transport", sub_type="car_petrol", quantity=50, unit="km", date=date.today()),
    ]
    response = process_message("How am I doing?", profile, activities)
    assert response.intent == "footprint_status"
    assert "kg CO" in response.reply
    assert len(response.suggested_actions) > 0


def test_insights_empty_state():
    profile = UserProfile()
    insights = generate_insights([], profile)
    assert len(insights) == 1
    assert "Start logging" in insights[0].title


def test_recommendations_with_transport():
    profile = UserProfile(primary_transport="car_petrol")
    activities = [
        ActivityLog(category="transport", sub_type="car_petrol", quantity=100, unit="km", date=date.today()),
    ]
    recs = generate_recommendations(activities, profile)
    assert len(recs) >= 1
    assert any(r.category == "transport" for r in recs)
