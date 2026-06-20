import sqlite3
import json
import uuid
from pathlib import Path
from datetime import date
from typing import Optional

from app.models import ActivityLog, UserProfile

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_FILE = DATA_DIR / "ecoguide.db"
PROFILE_FILE = DATA_DIR / "profile.json"
ACTIVITIES_FILE = DATA_DIR / "activities.json"

DEFAULT_PROFILE = UserProfile(name="Alex", household_size=1)


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    _ensure_data_dir()
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    _ensure_data_dir()
    db_exists = DB_FILE.exists()
    
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                household_size INTEGER,
                primary_transport TEXT,
                diet_type TEXT,
                weekly_goal_kg REAL,
                home_type TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id TEXT PRIMARY KEY,
                category TEXT,
                sub_type TEXT,
                quantity REAL,
                unit TEXT,
                date TEXT,
                notes TEXT
            )
        """)
        conn.commit()

    if not db_exists:
        migrate_json_data()


def migrate_json_data() -> None:
    try:
        if PROFILE_FILE.exists():
            data = json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
            profile = UserProfile.from_dict(data)
            save_profile(profile)
    except Exception:
        pass

    try:
        if ACTIVITIES_FILE.exists():
            data = json.loads(ACTIVITIES_FILE.read_text(encoding="utf-8"))
            activities = [ActivityLog.from_dict(item) for item in data]
            save_activities(activities)
    except Exception:
        pass


def load_profile() -> UserProfile:
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, household_size, primary_transport, diet_type, weekly_goal_kg, home_type FROM profile LIMIT 1")
        row = cursor.fetchone()
        if not row:
            save_profile(DEFAULT_PROFILE)
            return DEFAULT_PROFILE
        return UserProfile(
            name=row["name"],
            household_size=row["household_size"],
            primary_transport=row["primary_transport"],
            diet_type=row["diet_type"],
            weekly_goal_kg=row["weekly_goal_kg"],
            home_type=row["home_type"]
        )


def save_profile(profile: UserProfile) -> UserProfile:
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM profile")
        conn.execute("""
            INSERT INTO profile (name, household_size, primary_transport, diet_type, weekly_goal_kg, home_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (profile.name, profile.household_size, profile.primary_transport, profile.diet_type, profile.weekly_goal_kg, profile.home_type))
        conn.commit()
    return profile


def load_activities(days: Optional[int] = None) -> list[ActivityLog]:
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        if days is not None and days > 0:
            from datetime import timedelta
            cutoff = (date.today() - timedelta(days=days)).isoformat()
            cursor.execute("SELECT id, category, sub_type, quantity, unit, date, notes FROM activities WHERE date >= ? ORDER BY date DESC", (cutoff,))
        else:
            cursor.execute("SELECT id, category, sub_type, quantity, unit, date, notes FROM activities ORDER BY date DESC")
        
        rows = cursor.fetchall()
        return [
            ActivityLog(
                id=row["id"],
                category=row["category"],
                sub_type=row["sub_type"],
                quantity=row["quantity"],
                unit=row["unit"],
                date=date.fromisoformat(row["date"]),
                notes=row["notes"]
            )
            for row in rows
        ]


def save_activities(activities: list[ActivityLog]) -> list[ActivityLog]:
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM activities")
        for a in activities:
            if not a.id:
                a.id = str(uuid.uuid4())[:8]
            conn.execute("""
                INSERT INTO activities (id, category, sub_type, quantity, unit, date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (a.id, a.category, a.sub_type, a.quantity, a.unit, a.date.isoformat(), a.notes))
        conn.commit()
    return activities


def add_activity(activity: ActivityLog) -> ActivityLog:
    init_db()
    if not activity.id:
        activity.id = str(uuid.uuid4())[:8]
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO activities (id, category, sub_type, quantity, unit, date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (activity.id, activity.category, activity.sub_type, activity.quantity, activity.unit, activity.date.isoformat(), activity.notes))
        conn.commit()
    return activity


def delete_activity(activity_id: str) -> bool:
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        conn.commit()
        return cursor.rowcount > 0

