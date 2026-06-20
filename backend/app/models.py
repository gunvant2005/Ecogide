from dataclasses import asdict, dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class TransportMode(str, Enum):
    car_petrol = "car_petrol"
    car_electric = "car_electric"
    bus = "bus"
    train = "train"
    bike = "bike"
    walk = "walk"
    flight_short = "flight_short"
    flight_long = "flight_long"


class MealType(str, Enum):
    beef = "beef"
    pork = "pork"
    chicken = "chicken"
    fish = "fish"
    vegetarian = "vegetarian"
    vegan = "vegan"


class ActivityCategory(str, Enum):
    transport = "transport"
    food = "food"
    energy = "energy"
    shopping = "shopping"


@dataclass
class UserProfile:
    name: str = "User"
    household_size: int = 1
    primary_transport: str = "car_petrol"
    diet_type: str = "chicken"
    weekly_goal_kg: float = 80.0
    home_type: str = "apartment"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        return cls(
            name=data.get("name", "User"),
            household_size=int(data.get("household_size", 1)),
            primary_transport=data.get("primary_transport", "car_petrol"),
            diet_type=data.get("diet_type", "chicken"),
            weekly_goal_kg=float(data.get("weekly_goal_kg", 80.0)),
            home_type=data.get("home_type", "apartment"),
        )


@dataclass
class ActivityLog:
    category: str
    sub_type: str
    quantity: float
    unit: str
    date: date
    notes: str = ""
    id: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["date"] = self.date.isoformat()
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "ActivityLog":
        raw_date = data["date"]
        if isinstance(raw_date, str):
            parsed = date.fromisoformat(raw_date)
        else:
            parsed = raw_date
        return cls(
            id=data.get("id"),
            category=data["category"],
            sub_type=data["sub_type"],
            quantity=float(data["quantity"]),
            unit=data["unit"],
            date=parsed,
            notes=data.get("notes", ""),
        )


@dataclass
class AssistantResponse:
    reply: str
    suggested_actions: list[str] = field(default_factory=list)
    intent: str = "general"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FootprintSummary:
    total_kg: float
    by_category: dict[str, float]
    period_days: int
    vs_benchmark_pct: float
    vs_goal_pct: float
    top_category: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Insight:
    title: str
    description: str
    impact_kg: float
    priority: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Recommendation:
    action: str
    category: str
    estimated_savings_kg: float
    difficulty: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)
