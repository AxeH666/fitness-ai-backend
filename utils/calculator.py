def calculate_bmr_tdee_macros(data):
    weight = data["weight"]
    height = data["height"]
    age = data["age"]
    gender = data["gender"].lower()
    activity_level = data["activity_level"].lower()
    goal = data["fitness_goal"].lower()

    # BMR Calculation
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Activity multiplier
    activity_multipliers = {
        "sedentary": 1.2,
        "moderate": 1.55,
        "active": 1.725
    }
    multiplier = activity_multipliers.get(activity_level, 1.2)

    # Total Daily Energy Expenditure
    tdee = bmr * multiplier
    calories = round(tdee)

    # Macro % by goal
    macro_splits = {
        "lose fat": (40, 30, 30),
        "gain muscle": (35, 40, 25),
        "maintain": (30, 40, 30)
    }
    protein_pct, carbs_pct, fats_pct = macro_splits.get(goal, (30, 40, 30))

    # Calculate macros in grams
    protein_g = round((protein_pct / 100) * calories / 4)
    carbs_g = round((carbs_pct / 100) * calories / 4)
    fats_g = round((fats_pct / 100) * calories / 9)

    return {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "calories": calories,
        "macros": {
            "protein_g": protein_g,
            "carbs_g": carbs_g,
            "fats_g": fats_g,
            "split": {
                "protein_percent": protein_pct,
                "carbs_percent": carbs_pct,
                "fats_percent": fats_pct
            }
        }
    }
