from flask import Blueprint, jsonify
import random
from utils.workouts_data import workout_library
from utils.user_profile import load_user_profile, log_message
from utils.menstrual import estimate_cycle_phase
from routes.auth import require_api_key

workouts_bp = Blueprint("workouts", __name__)

@workouts_bp.route("/", methods=["POST"])
@require_api_key  # ✅ Protect this route
def generate_workout_plan():
    data = load_user_profile()

    goal = data.get("fitness_goal", "Maintain")
    days = int(data.get("days_available", 3))
    equipment = data.get("equipment_available", "bodyweight").lower()
    experience = data.get("experience_level", "beginner").lower()
    gender = data.get("gender", "unspecified")
    injuries = data.get("injuries", "").lower()

    # Menstrual phase logic
    is_disrupted = data.get("is_cycle_disrupted", False)
    last_period_start = data.get("last_period_start")
    menstrual_phase = (
        estimate_cycle_phase(last_period_start)
        if not is_disrupted and gender.lower() == "female" and last_period_start
        else None
    )

    # Step 1: Define workout split
    if days == 2:
        split = ["Full Body A", "Full Body B"]
    elif days == 3:
        split = ["Push", "Pull", "Legs"]
    elif days >= 4:
        split = ["Upper", "Lower", "Push", "Pull", "Legs", "Core"][:days]
    else:
        split = ["Full Body"]

    # Step 2: Generate plan
    workout_plan = {}

    for i, day in enumerate(split, 1):
        day_key = f"day_{i}"
        category = day.lower().split()[0]  # "push", "pull", etc.

        all_exercises = workout_library.get(category, {}).get(equipment, [])

        # Step 3: Injury filtering (e.g., skip deadlifts if back issues)
        filtered = []
        for ex in all_exercises:
            if "back" in injuries and "deadlift" in ex["name"].lower():
                continue
            if "knee" in injuries and "lunge" in ex["name"].lower():
                continue
            filtered.append(ex)

        # Step 4: Fallback if too few remain
        if len(filtered) < 3:
            filtered = all_exercises

        # Step 5: Sample and structure
        selected = random.sample(filtered, min(len(filtered), 3))

        detailed_exercises = []
        for ex in selected:
            detailed_exercises.append({
                "name": ex["name"],
                "muscle_group": ex["muscle_group"],
                "sets": 3 if experience == "beginner" else 4,
                "reps": "10–12" if goal == "gain muscle" else "12–15",
                "rest": "60–90 sec" if experience == "beginner" else "90–120 sec",
                "tempo": "2-0-2"
            })

        workout_plan[day_key] = {
            "split": day,
            "exercises": detailed_exercises
        }

    # Step 6: Menstrual guidance text
    notes = ""
    if menstrual_phase:
        if menstrual_phase.lower() in ["menstrual", "luteal"]:
            notes = "Focus on moderate volume and prioritize recovery. You may reduce intensity or skip high-impact work."
        elif menstrual_phase.lower() in ["follicular", "ovulation"]:
            notes = "This is a high-energy phase. You can push strength or intensity if feeling good."

    # ✅ Save to logs
    log_message("workout_plan", {
        "plan": workout_plan,
        "menstrual_guidance": notes if notes else None
    })

    return jsonify({
        "plan": workout_plan,
        "menstrual_guidance": notes if notes else None
    })
