import os
import requests
import json
from flask import Blueprint, jsonify
from dotenv import load_dotenv
from utils.user_profile import load_user_profile, log_message
from utils.menstrual import estimate_cycle_phase
from routes.auth import require_api_key

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

meals_bp = Blueprint("meals", __name__)

@meals_bp.route("", methods=["POST"])
@require_api_key  # ✅ Apply API key protection
def generate_meal_plan():
    user = load_user_profile()

    # Required fields
    age = user.get("age")
    height = user.get("height")
    weight = user.get("weight")

    if not all([age, height, weight]):
        return jsonify({"error": "Missing required fields: age, height, or weight"}), 400

    # Safe string fields with fallback
    gender = user.get("gender", "Unspecified") or "Unspecified"
    activity_level = user.get("activity_level", "Moderate") or "Moderate"
    fitness_goal = user.get("fitness_goal", "Maintain") or "Maintain"
    dietary_preference = user.get("dietary_preference", "Non-Vegetarian") or "Non-Vegetarian"

    # Nutrition targets
    calories = user.get("calories")
    macros = user.get("macros", {})
    protein = macros.get("protein_g", 0)
    carbs = macros.get("carbs_g", 0)
    fats = macros.get("fats_g", 0)

    # Personalization
    meals_per_day = user.get("meals_per_day", 4)
    fasting_window = user.get("fasting_window", None)
    preferred_cuisines = user.get("preferred_cuisines", [])
    foods_to_avoid = user.get("foods_to_avoid", [])

    fasting_text = f"\nThe user follows intermittent fasting and eats only between {fasting_window}." if fasting_window else ""
    cuisines_text = f"\nPreferred cuisines: {', '.join(preferred_cuisines)}." if preferred_cuisines else ""
    avoid_text = f"\nAvoid the following foods: {', '.join(foods_to_avoid)}." if foods_to_avoid else ""

    # Prompt
    prompt = f"""
Generate a meal plan with {meals_per_day} meals for a {age}-year-old {gender.lower()} who wants to {fitness_goal.lower()}.
They are {height} cm tall, weigh {weight} kg, and are {activity_level.lower()} active.

Daily nutritional targets:
- Calories: {calories} kcal
- Protein: {protein}g
- Carbs: {carbs}g
- Fats: {fats}g

Dietary preference: {dietary_preference}.{fasting_text}{cuisines_text}{avoid_text}

Return ONLY valid JSON with the following fields:
- meal_1
- meal_2
- ...
(based on number of meals)

Each meal must include:
- dish (string)
- ingredients (list of strings)
- calories (int)
- protein (int)
- carbs (int)
- fats (int)

DO NOT include explanations, markdown, or backticks. Only output raw JSON.
Ensure the JSON is valid and all keys are properly quoted and escaped.
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful nutrition assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        try:
            parsed = json.loads(content)
            log_message("meal_plan", parsed)
            return jsonify(parsed)
        except json.JSONDecodeError:
            log_message("meal_plan_raw", content)
            return jsonify({
                "raw_output": content,
                "warning": "Could not parse as JSON. Model may have returned extra text."
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
