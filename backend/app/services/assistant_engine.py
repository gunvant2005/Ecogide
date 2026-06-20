import re

from app.constants import CATEGORY_LABELS, FOOD, TRANSPORT, WEEKLY_BENCHMARK
from app.models import ActivityLog, AssistantResponse, UserProfile
from app.services.carbon_calculator import summarize_footprint
from app.services.insights_engine import generate_recommendations


INTENT_PATTERNS: list[tuple[str, list[str]]] = [
    ("greeting", [r"\b(hi|hello|hey|good morning|good evening)\b"]),
    ("reduce_tips", [r"\b(reduce|lower|cut|save|improve|help me|what should|tips|advice)\b"]),
    ("goal_progress", [r"\b(goal|target|on track|progress)\b"]),
    ("footprint_status", [r"\b(how am i|my footprint|how much|total|status|doing)\b"]),
    ("transport_help", [r"\b(commute|drive|car|bus|train|bike|transport|travel|flight)\b"]),
    ("log_help", [r"\b(log|track|record|add activity)\b"]),
    ("food_help", [r"\b(food|meal|eat|diet|beef|vegan|vegetarian|meat)\b"]),
    ("energy_help", [r"\b(energy|electric|heat|power|home|thermostat)\b"]),
    ("explain", [r"\b(what is|explain|why|how does|carbon|co2|emission)\b"]),
]


def detect_intent(message: str) -> str:
    text = message.lower().strip()
    for intent, patterns in INTENT_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, text):
                return intent
    return "general"


def _format_category_breakdown(summary) -> str:
    lines = []
    for cat, kg in summary.by_category.items():
        if kg > 0:
            label = CATEGORY_LABELS.get(cat, cat)
            pct = kg / summary.total_kg * 100 if summary.total_kg else 0
            lines.append(f"• {label}: {kg} kg ({pct:.0f}%)")
    return "\n".join(lines) if lines else "No activities logged yet."


def _footprint_reply(activities: list[ActivityLog], profile: UserProfile) -> AssistantResponse:
    summary = summarize_footprint(activities, days=7, weekly_goal=profile.weekly_goal_kg)
    if summary.total_kg == 0:
        return AssistantResponse(
            reply=(
                f"Hi {profile.name}! You haven't logged any activities in the last 7 days. "
                "Start by logging a commute or meal — I'll analyze your footprint instantly."
            ),
            suggested_actions=[
                "Log today's commute",
                "Log a meal",
                "Set a weekly goal",
            ],
            intent="footprint_status",
        )

    benchmark_note = (
        f"{abs(summary.vs_benchmark_pct):.0f}% {'above' if summary.vs_benchmark_pct > 0 else 'below'} "
        f"the typical urban benchmark ({WEEKLY_BENCHMARK} kg/week)."
    )
    top_label = CATEGORY_LABELS.get(summary.top_category or "", "transport")

    return AssistantResponse(
        reply=(
            f"Over the last 7 days you've emitted **{summary.total_kg} kg CO₂e**.\n\n"
            f"{_format_category_breakdown(summary)}\n\n"
            f"Your biggest category is **{top_label}**. You're {benchmark_note}\n"
            f"Compared to your goal of {profile.weekly_goal_kg} kg/week, "
            f"you're {summary.vs_goal_pct:+.0f}%."
        ),
        suggested_actions=[
            f"Tips to reduce {top_label.lower()}",
            "Show my top recommendations",
            "How do I compare to average?",
        ],
        intent="footprint_status",
    )


def _goal_reply(activities: list[ActivityLog], profile: UserProfile) -> AssistantResponse:
    summary = summarize_footprint(activities, days=7, weekly_goal=profile.weekly_goal_kg)
    remaining = round(profile.weekly_goal_kg - summary.total_kg, 1)

    if summary.total_kg == 0:
        return AssistantResponse(
            reply=f"Your weekly goal is {profile.weekly_goal_kg} kg CO₂e. Log activities to track progress.",
            suggested_actions=["Log an activity", "What is a realistic goal?"],
            intent="goal_progress",
        )

    if remaining >= 0:
        reply = (
            f"You have **{remaining} kg** left in your weekly budget "
            f"({summary.total_kg} / {profile.weekly_goal_kg} kg used). Stay on course!"
        )
    else:
        reply = (
            f"You're **{abs(remaining)} kg over** your weekly goal. "
            "Focus on one swap in your highest category to recover."
        )

    return AssistantResponse(
        reply=reply,
        suggested_actions=["What should I change?", "Show transport tips"],
        intent="goal_progress",
    )


def _transport_reply(activities: list[ActivityLog], profile: UserProfile) -> AssistantResponse:
    summary = summarize_footprint(activities, days=7)
    transport_kg = summary.by_category.get("transport", 0)
    mode = profile.primary_transport.replace("_", " ")

    car_km_equiv = round(transport_kg / TRANSPORT.get(profile.primary_transport, 0.21))
    train_savings = round(10 * (TRANSPORT["car_petrol"] - TRANSPORT["train"]), 1)

    reply = (
        f"Your primary mode is **{mode}**. Transport logged: **{transport_kg} kg** this week"
        + (f" (~{car_km_equiv} km equivalent)." if transport_kg else ".")
        + f"\n\nSwitching 10 km from car to train saves about **{train_savings} kg**. "
        "Combining errands into one trip can cut 15–20% of car emissions."
    )

    return AssistantResponse(
        reply=reply,
        suggested_actions=["Log a bike trip", "Compare car vs train", "Reduce my footprint"],
        intent="transport_help",
    )


def _food_reply(profile: UserProfile) -> AssistantResponse:
    diet = profile.diet_type
    beef_cost = FOOD["beef"]
    vegan_cost = FOOD["vegan"]

    reply = (
        f"Your profile diet is **{diet}**. A beef meal emits ~{beef_cost} kg vs "
        f"~{vegan_cost} kg for vegan — a **{beef_cost - vegan_cost:.1f} kg** difference per meal.\n\n"
        "Try 'Meatless Monday' or swap beef for chicken (saves ~4 kg per meal)."
    )

    return AssistantResponse(
        reply=reply,
        suggested_actions=["Log a vegetarian meal", "Food reduction tips"],
        intent="food_help",
    )


def _reduce_reply(activities: list[ActivityLog], profile: UserProfile) -> AssistantResponse:
    recs = generate_recommendations(activities, profile)
    lines = [f"**{i + 1}. {r.action}** (~{r.estimated_savings_kg} kg saved, {r.difficulty})" for i, r in enumerate(recs[:3])]
    reply = "Based on your profile and recent logs, prioritize:\n\n" + "\n".join(lines)
    actions = [r.action for r in recs[:2]] + ["Show my full footprint"]

    return AssistantResponse(
        reply=reply,
        suggested_actions=actions,
        intent="reduce_tips",
    )


def _explain_reply() -> AssistantResponse:
    return AssistantResponse(
        reply=(
            "**Carbon footprint** measures greenhouse gases (CO₂e) from your activities.\n\n"
            "Major sources: transport (fuel), food (especially red meat), home energy, and goods.\n\n"
            "This app uses standard emission factors to estimate impact and suggests "
            "personalized swaps based on *your* highest-impact categories."
        ),
        suggested_actions=["How am I doing?", "Tips to reduce", "Log an activity"],
        intent="explain",
    )


def process_message(
    message: str,
    profile: UserProfile,
    activities: list[ActivityLog],
) -> AssistantResponse:
    intent = detect_intent(message)

    if intent == "greeting":
        return AssistantResponse(
            reply=(
                f"Hello {profile.name}! I'm EcoGuide, your carbon footprint assistant. "
                "Ask about your footprint, get reduction tips, or learn how emissions work."
            ),
            suggested_actions=["How am I doing?", "Tips to reduce my footprint", "Explain carbon footprint"],
            intent="greeting",
        )

    if intent == "footprint_status":
        return _footprint_reply(activities, profile)

    if intent == "goal_progress":
        return _goal_reply(activities, profile)

    if intent == "transport_help":
        return _transport_reply(activities, profile)

    if intent == "food_help":
        return _food_reply(profile)

    if intent == "energy_help":
        return AssistantResponse(
            reply=(
                "Home energy tips:\n"
                "• Lower heating 1°C → ~8% savings\n"
                "• Unplug idle devices → ~5% savings\n"
                "• LED bulbs use 75% less than incandescent\n\n"
                "Log kWh from your utility bill for accurate tracking."
            ),
            suggested_actions=["Log electricity usage", "How am I doing?"],
            intent="energy_help",
        )

    if intent == "reduce_tips":
        return _reduce_reply(activities, profile)

    if intent == "explain":
        return _explain_reply()

    if intent == "log_help":
        return AssistantResponse(
            reply=(
                "Log activities from the **Log Activity** tab:\n"
                "• **Transport** — km traveled by car, bus, train, etc.\n"
                "• **Food** — number of meals by type\n"
                "• **Energy** — kWh electricity or gas\n"
                "• **Shopping** — items purchased\n\n"
                "The more you log, the smarter my recommendations become."
            ),
            suggested_actions=["How am I doing?", "Tips to reduce"],
            intent="log_help",
        )

    return _reduce_reply(activities, profile)
