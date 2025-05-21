from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .database import init_db, get_all_users, register_user, verify_user

app = FastAPI()

# ініціалізуємо БД при запуску сервера
init_db()

class User(BaseModel):
    username: str
    password: str

@app.get("/users")
def read_users():
    return get_all_users()

@app.post("/register")
def register(user: User):
    user_id = register_user(user.username, user.password)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully", "user_id": user_id}
@app.post("/login")
def login(user: User):
    user_data = verify_user(user.username, user.password)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful!", "user_id": user_data["id"], "username": user_data["username"]}

