from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List

router = APIRouter(prefix='/users', tags=['Users'])

users_db = [
    {"id": 1, "username": "admin", "email": "admin@example.com", "full_name": "Asosiy Admin", "is_active": True},
    {"id": 2, "username": "user1", "email": "user1@test.uz", "full_name": "Abbos Akromov", "is_active": True},
]


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


@router.get('/', response_model=List[UserBase])
async def users_list():
    return users_db


@router.get('/{username}', response_model=UserBase)
async def user_detail(username: str):
    user = next((u for u in users_db if u['username'] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail='Foydalanuvchi topilmadi')
    return user


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    if any(u['username'] == user_data.username for u in users_db):
        raise HTTPException(status_code=400, detail="Ushbu username allaqachon band")

    new_user = {
        "id": len(users_db) + 1,
        **user_data.dict(),
        "is_active": True
    }
    users_db.append(new_user)
    return {"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz", "user": user_data.username}


@router.patch('/{username}/update')
async def update_profile(username: str, data: UserUpdate):
    user = next((u for u in users_db if u['username'] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail='Foydalanuvchi topilmadi')

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        user[key] = value

    return {"message": "Profil yangilandi", "user": user}


@router.delete('/{username}/deactivate')
async def deactivate_user(username: str):
    user = next((u for u in users_db if u['username'] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail='Foydalanuvchi topilmadi')

    user['is_active'] = False
    return {"message": f"{username} akkaunti faolsizlantirildi"}