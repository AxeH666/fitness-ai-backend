import os
import requests
from flask import Blueprint, jsonify
from dotenv import load_dotenv
from utils.user_profile import load_user_profile, log_message
from utils.menstrual import estimate_cycle_phase
from routes.auth import require_api_key

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

motivation_bp = Blueprint("motivation", __name__)

@motivation_bp.route("", methods=["GET"])
@require_api_key  # ✅ Protect the route
def daily_message():
    user = load_user_profile()

    age = user.get("age")
    gender = user.get("gender", "Unspecified").lower()
    goal = user.get("fitness_goal", "Maintain")
    is_disrupted = user.get("is_cycle_disrupted", False)
    last_period_start = user.get("last_period_start")
    cycle_phase = (
        estimate_cycle_phase(last_period_start)
        if not is_disrupted and gender == "female" and last_period_start
        else None
    )

    # 🔁 Prompt: cycle-aware and goal-aware
    prompt = f"""
You are a motivational fitness coach. Write a short, uplifting message (1-2 sentences max) for a {age}-year-old {gender} whose fitness goal is to {goal.lower()}.

{"Her menstrual phase is " + cycle_phase + "." if cycle_phase else ""}

Avoid cliches. Be specific. Use energy-aware language if cycle is mentioned. Never include markdown or explanations.
Return only the motivational message as plain text.
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a compassionate, clear, science-based fitness motivator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        message = response.json()["choices"][0]["message"]["content"].strip()

        # ✅ Save log
        log_message("daily_message", message)

        return jsonify({"message": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
