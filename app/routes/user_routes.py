from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.database.json_handler import read_users, write_users

router = APIRouter(prefix="/users", tags=["Users"])

# GET all users
@router.get("/", response_model=list[UserResponse])
def get_users():
    users = read_users()
    return users

# GET single user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    users = read_users()
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# CREATE new user
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    users = read_users()
    new_id = max([u["id"] for u in users], default=0) + 1
    new_user = user.dict()
    new_user["id"] = new_id
    users.append(new_user)
    write_users(users)
    return new_user

# UPDATE user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    users = read_users()
    for idx, u in enumerate(users):
        if u["id"] == user_id:
            updated_user = u.copy()
            update_data = user_update.dict(exclude_unset=True)
            updated_user.update(update_data)
            users[idx] = updated_user
            write_users(users)
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# DELETE user
@router.delete("/{user_id}")
def delete_user(user_id: int):
    users = read_users()
    for idx, u in enumerate(users):
        if u["id"] == user_id:
            users.pop(idx)
            write_users(users)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
