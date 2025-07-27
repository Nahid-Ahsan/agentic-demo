from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt  # Ensure this is from PyJWT
from schema.user_schemas import UserCreate, User
from service.db_service import get_database
import os

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user: UserCreate):
    db = await get_database()
    # Check if username or email already exists
    if await db.users.find_one({"$or": [{"username": user.username}, {"email": user.email}]}):
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    
    result = await db.users.insert_one(user_dict)
    return User(**user_dict, id=str(result.inserted_id))

async def authenticate_user(username: str, password: str):
    db = await get_database()
    user = await db.users.find_one({"username": username})
    if not user:
        return False
    if not pwd_context.verify(password, user["hashed_password"]):
        return False
    return User(**user, id=str(user["_id"]))

async def create_access_token(data: dict):
    """
    Create a JWT token with the provided data and expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt