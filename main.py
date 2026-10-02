from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users_db = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: str = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    workout_plan = f"Day 1: Full Body Workout ({intensity} intensity). Day 2: Core & Cardio. Day 3: Rest."
    nutrition_tip = "Prioritize protein intake in every meal (chicken, fish, beans, or Greek yogurt) for muscle building and metabolic support."

    users_db[user_id] = {
        "name": name,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "original_plan": workout_plan,
        "updated_plan": workout_plan,
        "nutrition_tip": nutrition_tip
    }

    return templates.TemplateResponse("workout.html", {"request": request, "user": users_db[user_id]})

@app.get("/feedback", response_class=HTMLResponse)
async def feedback_page(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request, "message": None})

@app.post("/feedback", response_class=HTMLResponse)
async def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...)):
    message = None
    if user_id in users_db:
        users_db[user_id]["updated_plan"] += f" [Updated based on feedback: {feedback}]"
        message = "Your workout plan has been successfully updated based on your feedback!"
    else:
        message = "User ID not found."
    return templates.TemplateResponse("feedback.html", {"request": request, "message": message})

@app.get("/users", response_class=HTMLResponse)
async def view_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db})