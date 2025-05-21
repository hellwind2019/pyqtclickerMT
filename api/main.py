from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .database import init_db, get_all_users, register_user

app = FastAPI()

# ініціалізуємо БД при запуску сервера
init_db()

class UserRegister(BaseModel):
    username: str
    password: str

@app.get("/users")
def read_users():
    return get_all_users()

@app.post("/register")
def register(user: UserRegister):
    user_id = register_user(user.username, user.password)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully", "user_id": user_id}
