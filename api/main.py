from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .database import init_db, get_all_users, register_user, verify_user, update_user_state, get_user_state

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

class UserState(BaseModel):
    score: int
    multiplier: int
    multiplier_price: int
    boost_multiplier: int
    boost_price: int
    boost_active: bool
    auto_click: int
    auto_click_price: int

@app.get("/user/{user_id}/state")
def get_state(user_id: int):
    state = get_user_state(user_id)
    if state is None:
        raise HTTPException(status_code=404, detail="User not found")
    return state

@app.post("/user/{user_id}/state")
def update_state(user_id: int, state: UserState):
    success = update_user_state(
        user_id,
        state.score,
        state.multiplier,
        state.multiplier_price,
        state.boost_multiplier,
        state.boost_price,
        state.boost_active,
        state.auto_click,
        state.auto_click_price
    )
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "State updated successfully"}
