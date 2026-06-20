from app.constants import CATEGORY_LABELS, TRANSPORT
from app.models import Insight, Recommendation, UserProfile
from app.services.carbon_calculator import summarize_footprint
from app.models import ActivityLog


def generate_insights(
    activities: list[ActivityLog],
    profile: UserProfile,
) -> list[Insight]:
    summary = summarize_footprint(activities, days=7, weekly_goal=profile.weekly_goal_kg)
    insights: list[Insight] = []

    if summary.total_kg == 0:
        insights.append(
            Insight(
                title="Start logging your activities",
                description=(
                    "Log transport, meals, energy, and shopping to unlock "
                    "personalized insights about your carbon footprint."
                ),
                impact_kg=0,
                priority="high",
            )
        )
        return insights

    if summary.vs_benchmark_pct > 10:
        insights.append(
            Insight(
                title="Above average footprint",
                description=(
                    f"Your last 7 days total {summary.total_kg} kg CO₂e, "
                    f"{summary.vs_benchmark_pct:.0f}% above the urban benchmark. "
                    f"Focus on {CATEGORY_LABELS.get(summary.top_category or '', 'transport')} first."
                ),
                impact_kg=round(summary.total_kg - 120, 1),
                priority="high",
            )
        )
    elif summary.vs_benchmark_pct < -10:
        insights.append(
            Insight(
                title="Below average — great progress",
                description=(
                    f"You're {abs(summary.vs_benchmark_pct):.0f}% below the typical "
                    f"urban professional benchmark. Keep up sustainable habits."
                ),
                impact_kg=0,
                priority="low",
            )
        )

    if summary.vs_goal_pct > 0:
        over = round(summary.total_kg - profile.weekly_goal_kg, 1)
        insights.append(
            Insight(
                title="Weekly goal exceeded",
                description=(
                    f"You are {over} kg over your {profile.weekly_goal_kg} kg goal. "
                    "Small swaps in your highest category can close the gap."
                ),
                impact_kg=over,
                priority="high" if over > 15 else "medium",
            )
        )

    transport_kg = summary.by_category.get("transport", 0)
    if transport_kg > summary.total_kg * 0.4:
        insights.append(
            Insight(
                title="Transport is your biggest lever",
                description=(
                    f"Transport accounts for {transport_kg} kg ({transport_kg / summary.total_kg * 100:.0f}%) "
                    "of your footprint. Even one car-free day saves meaningful emissions."
                ),
                impact_kg=round(transport_kg * 0.2, 1),
                priority="high",
            )
        )

    food_kg = summary.by_category.get("food", 0)
    if food_kg > 20:
        insights.append(
            Insight(
                title="Diet shifts add up quickly",
                description=(
                    f"Food contributes {food_kg} kg this week. Replacing one beef meal "
                    "with a plant-based option saves roughly 5.5 kg CO₂e."
                ),
                impact_kg=5.5,
                priority="medium",
            )
        )

    return insights[:5]


def generate_recommendations(
    activities: list[ActivityLog],
    profile: UserProfile,
) -> list[Recommendation]:
    summary = summarize_footprint(activities, days=7, weekly_goal=profile.weekly_goal_kg)
    recs: list[Recommendation] = []

    top = summary.top_category or "transport"
    transport_kg = summary.by_category.get("transport", 0)

    if top == "transport" or profile.primary_transport.startswith("car"):
        car_factor = TRANSPORT.get(profile.primary_transport, 0.21)
        train_savings = round(20 * (car_factor - TRANSPORT["train"]), 1)
        recs.append(
            Recommendation(
                action="Swap one 20 km commute from car to train this week",
                category="transport",
                estimated_savings_kg=max(train_savings, 2.0),
                difficulty="moderate",
                reason="Transport is your highest-impact category based on recent logs.",
            )
        )
        if transport_kg > 15:
            recs.append(
                Recommendation(
                    action="Try biking or walking trips under 3 km",
                    category="transport",
                    estimated_savings_kg=round(6 * car_factor, 1),
                    difficulty="easy",
                    reason="Short trips have high per-km emissions when driving solo.",
                )
            )

    if top == "food" or profile.diet_type in ("beef", "pork"):
        recs.append(
            Recommendation(
                action="Replace 2 beef meals with vegetarian options",
                category="food",
                estimated_savings_kg=11.0,
                difficulty="easy",
                reason="Red meat has the highest food-related emissions.",
            )
        )

    energy_kg = summary.by_category.get("energy", 0)
    if top == "energy" or energy_kg > 10:
        recs.append(
            Recommendation(
                action="Lower thermostat by 1°C for the week",
                category="energy",
                estimated_savings_kg=round(energy_kg * 0.08, 1) if energy_kg else 3.0,
                difficulty="easy",
                reason="Heating and cooling drive home energy emissions.",
            )
        )

    if summary.total_kg > profile.weekly_goal_kg:
        gap = round(summary.total_kg - profile.weekly_goal_kg, 1)
        recs.append(
            Recommendation(
                action=f"Pick one high-impact swap to cut {gap} kg this week",
                category=top,
                estimated_savings_kg=gap,
                difficulty="moderate",
                reason="You're over your personal weekly goal.",
            )
        )

    if not recs:
        recs.append(
            Recommendation(
                action="Maintain current habits and log daily",
                category="general",
                estimated_savings_kg=0,
                difficulty="easy",
                reason="You're on track — consistent tracking helps spot regressions early.",
            )
        )

    return recs[:4]
