from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os 
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") or "fallback-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(user_password):
    hashed_password = pwd_context.hash(user_password)
    return hashed_password

def verify_password(user_password, hashed_password):
    return pwd_context.verify(user_password, hashed_password)

def create_access_token(user_id: int):
    data = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(data, SECRET_KEY, algorithm = ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except JWTError:
        return None