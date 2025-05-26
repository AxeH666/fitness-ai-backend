from flask import Flask
from routes.calories import calories_bp
from routes.meals import meals_bp
from routes.workouts import workouts_bp
from routes.motivation import motivation_bp
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load API_KEY and GROQ_API_KEY from .env

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(calories_bp, url_prefix='/generate_calories_macros')
app.register_blueprint(meals_bp, url_prefix='/generate_meal_plan')
app.register_blueprint(workouts_bp, url_prefix='/generate_workout_plan')
app.register_blueprint(motivation_bp, url_prefix="/daily_message")

@app.route("/")
def home():
    return {"message": "Flask is working!"}

@app.errorhandler(404)
def not_found(e):
    return {"error": "Route not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)
