# AI-Powered Fitness Assistant (Backend MVP)

This is the backend system for an AI-powered personal fitness assistant. It generates personalized meal plans, workout routines, and motivational messages based on user profile data — including cycle-aware logic for female users. Powered by LLaMA 2 3B (via Groq), the app delivers secure, intelligent fitness advice with modular API endpoints.

---

## 🚀 Features
- 🧠 AI-generated meal plans (Groq + LLaMA 3)
- 🏋️ Workout plans based on goal, days, equipment, injuries, and menstrual phase
- 🔢 Calorie & macronutrient calculator (TDEE-based)
- 🌤️ Daily motivational message (gender + cycle-aware)
- 🔐 API key protected endpoints
- 💾 Persistent user profile & logs
- 🧱 Modular Flask backend using Blueprints

---

## 📦 Project Structure
```
server/
├── app.py
├── routes/
│   ├── meals.py
│   ├── workouts.py
│   ├── motivation.py
│   ├── calories.py
│   └── auth.py
├── utils/
│   ├── user_profile.py
│   ├── calculator.py
│   ├── workouts_data.py
│   └── menstrual.py
├── data/
│   └── user_profile.json
├── logs/
├── .env.example
├── requirements.txt
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**
```bash
git clone https://github.com/your-username/fitness-ai-backend.git
cd fitness-ai-app\server
```

2. **Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Copy `.env.example` to `.env` and add your API keys.

5. **Run the app**
```bash
python app.py
```

---

## 🔐 Environment Variables

In `.env`:

```
GROQ_API_KEY=your_groq_api_key_here
API_KEY=your_custom_api_key
```

---

## 📮 Endpoints

| Method | Route                       | Description              |
|--------|-----------------------------|--------------------------|
| POST   | `/generate_meal_plan`       | Returns meal plan JSON   |
| POST   | `/generate_workout_plan`    | Returns workout plan     |
| POST   | `/generate_calories_macros` | Returns calorie+macro    |
| GET    | `/daily_message`            | Returns motivational msg |

> **Note**: All endpoints require an `x-api-key` header.

---

## 🧠 Author

**Mohaddis Shaik**  
Aspiring AI Solutions Developer | Passionate about fitness & tech
