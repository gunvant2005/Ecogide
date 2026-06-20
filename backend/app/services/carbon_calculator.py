from datetime import date, timedelta

from app.constants import ENERGY, FOOD, SHOPPING, TRANSPORT, WEEKLY_BENCHMARK
from app.models import ActivityLog, FootprintSummary


def calculate_activity_emissions(activity: ActivityLog) -> float:
    qty = activity.quantity
    sub = activity.sub_type

    if activity.category == "transport":
        factor = TRANSPORT.get(sub, 0.15)
        return round(qty * factor, 2)

    if activity.category == "food":
        factor = FOOD.get(sub, 2.0)
        return round(qty * factor, 2)

    if activity.category == "energy":
        factor = ENERGY.get(sub, 0.42)
        return round(qty * factor, 2)

    if activity.category == "shopping":
        factor = SHOPPING.get(sub, 5.0)
        return round(qty * factor, 2)

    return 0.0


def summarize_footprint(
    activities: list[ActivityLog],
    days: int = 7,
    weekly_goal: float = 80.0,
) -> FootprintSummary:
    cutoff = date.today() - timedelta(days=days - 1)
    recent = [a for a in activities if a.date >= cutoff]

    by_category: dict[str, float] = {
        "transport": 0.0,
        "food": 0.0,
        "energy": 0.0,
        "shopping": 0.0,
    }

    total = 0.0
    for activity in recent:
        emissions = calculate_activity_emissions(activity)
        total += emissions
        by_category[activity.category] = by_category.get(activity.category, 0.0) + emissions

    for key in by_category:
        by_category[key] = round(by_category[key], 2)

    total = round(total, 2)
    benchmark_for_period = WEEKLY_BENCHMARK * (days / 7)
    goal_for_period = weekly_goal * (days / 7)

    vs_benchmark = (
        round((total - benchmark_for_period) / benchmark_for_period * 100, 1)
        if benchmark_for_period
        else 0.0
    )
    vs_goal = (
        round((total - goal_for_period) / goal_for_period * 100, 1)
        if goal_for_period
        else 0.0
    )

    top = max(by_category, key=by_category.get) if total > 0 else None
    if top and by_category[top] == 0:
        top = None

    return FootprintSummary(
        total_kg=total,
        by_category=by_category,
        period_days=days,
        vs_benchmark_pct=vs_benchmark,
        vs_goal_pct=vs_goal,
        top_category=top,
    )
