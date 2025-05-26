# utils/workouts_data.py

workout_library = {
    "push": {
        "bodyweight": [
            {"name": "Push-Ups", "muscle_group": "Chest"},
            {"name": "Incline Push-Ups", "muscle_group": "Upper Chest"},
            {"name": "Wall Push-Ups", "muscle_group": "Chest"}
        ],
        "dumbbells": [
            {"name": "Dumbbell Bench Press", "muscle_group": "Chest"},
            {"name": "Dumbbell Shoulder Press", "muscle_group": "Shoulders"},
            {"name": "Dumbbell Lateral Raise", "muscle_group": "Shoulders"}
        ],
        "gym": [
            {"name": "Barbell Bench Press", "muscle_group": "Chest"},
            {"name": "Shoulder Press Machine", "muscle_group": "Shoulders"},
            {"name": "Cable Chest Fly", "muscle_group": "Chest"}
        ]
    },
    "pull": {
        "bodyweight": [
            {"name": "Inverted Rows", "muscle_group": "Back"},
            {"name": "Negative Pull-Ups", "muscle_group": "Back"},
            {"name": "Superman Hold", "muscle_group": "Lower Back"}
        ],
        "dumbbells": [
            {"name": "Dumbbell Rows", "muscle_group": "Back"},
            {"name": "Bicep Curls", "muscle_group": "Biceps"},
            {"name": "Hammer Curls", "muscle_group": "Biceps"}
        ],
        "gym": [
            {"name": "Lat Pulldown", "muscle_group": "Back"},
            {"name": "Seated Cable Row", "muscle_group": "Back"},
            {"name": "EZ Bar Curl", "muscle_group": "Biceps"}
        ]
    },
    "legs": {
        "bodyweight": [
            {"name": "Bodyweight Squats", "muscle_group": "Quads"},
            {"name": "Glute Bridges", "muscle_group": "Glutes"},
            {"name": "Wall Sits", "muscle_group": "Quads"}
        ],
        "dumbbells": [
            {"name": "Goblet Squat", "muscle_group": "Quads"},
            {"name": "Dumbbell RDLs", "muscle_group": "Hamstrings"},
            {"name": "Dumbbell Lunges", "muscle_group": "Quads/Glutes"}
        ],
        "gym": [
            {"name": "Barbell Back Squat", "muscle_group": "Quads"},
            {"name": "Leg Press", "muscle_group": "Quads"},
            {"name": "Romanian Deadlift", "muscle_group": "Hamstrings"}
        ]
    },
    "core": {
        "bodyweight": [
            {"name": "Plank", "muscle_group": "Core"},
            {"name": "Mountain Climbers", "muscle_group": "Core"},
            {"name": "Leg Raises", "muscle_group": "Lower Abs"}
        ],
        "dumbbells": [
            {"name": "Weighted Russian Twists", "muscle_group": "Obliques"},
            {"name": "Dumbbell Side Bend", "muscle_group": "Obliques"}
        ],
        "gym": [
            {"name": "Cable Crunch", "muscle_group": "Abs"},
            {"name": "Decline Sit-ups", "muscle_group": "Abs"}
        ]
    }
}

# Add combined splits for full-body, upper, and lower training
workout_library["full_body"] = {
    "bodyweight": (
        workout_library["push"]["bodyweight"] +
        workout_library["pull"]["bodyweight"] +
        workout_library["legs"]["bodyweight"]
    ),
    "dumbbells": (
        workout_library["push"]["dumbbells"] +
        workout_library["pull"]["dumbbells"] +
        workout_library["legs"]["dumbbells"]
    ),
    "gym": (
        workout_library["push"]["gym"] +
        workout_library["pull"]["gym"] +
        workout_library["legs"]["gym"]
    )
}

workout_library["upper"] = {
    "bodyweight": (
        workout_library["push"]["bodyweight"] +
        workout_library["pull"]["bodyweight"]
    ),
    "dumbbells": (
        workout_library["push"]["dumbbells"] +
        workout_library["pull"]["dumbbells"]
    ),
    "gym": (
        workout_library["push"]["gym"] +
        workout_library["pull"]["gym"]
    )
}

workout_library["lower"] = {
    "bodyweight": workout_library["legs"]["bodyweight"],
    "dumbbells": workout_library["legs"]["dumbbells"],
    "gym": workout_library["legs"]["gym"]
}
