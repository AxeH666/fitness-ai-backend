import json
import os
from flask import abort
from datetime import datetime

PROFILE_PATH = os.path.join("data", "user_profile.json")

REQUIRED_FIELDS = [
    "age", "gender", "height", "weight", "fitness_goal", "activity_level",
    "days_available", "equipment_available", "experience_level", "dietary_preference"
]

def load_user_profile():
    if not os.path.exists(PROFILE_PATH):
        abort(400, description="User profile not found.")

    try:
        with open(PROFILE_PATH, "r") as f:
            profile = json.load(f)

        # Basic presence check
        missing = [field for field in REQUIRED_FIELDS if field not in profile]
        if missing:
            abort(400, description=f"Missing required fields: {', '.join(missing)}")

        # Numeric validation
        if profile["age"] <= 0 or profile["height"] <= 0 or profile["weight"] <= 0:
            abort(400, description="Invalid values for age, height, or weight.")

        # Optional: basic goal validation
        if profile["fitness_goal"].lower() not in ["lose fat", "gain muscle", "maintain"]:
            abort(400, description="Invalid fitness_goal.")

        return profile

    except json.JSONDecodeError:
        abort(400, description="Invalid JSON in user_profile.json.")
    except Exception as e:
        abort(500, description=str(e))


def log_message(tag, content):
    """Utility to save messages/responses into /logs with timestamps."""
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join("logs", f"{tag}_{now}.txt")
    
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(content, dict):
            json.dump(content, f, indent=2)  # Save dicts cleanly
        else:
            f.write(str(content))  # Handle strings or simple values
