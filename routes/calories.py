from flask import Blueprint, jsonify
from utils.calculator import calculate_bmr_tdee_macros
from utils.user_profile import load_user_profile
from routes.auth import require_api_key

calories_bp = Blueprint("calories", __name__)

@calories_bp.route("", methods=["POST"])
@require_api_key  # ✅ Protect the route
def generate_calories_macros():
    # 🔁 Load all user data from stored profile
    data = load_user_profile()

    # ✅ Pass it to the calculator function
    result = calculate_bmr_tdee_macros(data)

    return jsonify(result)
