from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import uuid

from .models import UserCreate, UserResponse
from .db import user_collection
from .auth import create_token
from .utils import hash_password

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"mensaje": "Error interno del servidor"})

@app.post("/users", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate):
    # Verificar email duplicado
    if user_collection.find_one({"email": user.email}):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"mensaje": "El correo ya registrado"}
        )
    

    now = datetime.now(timezone.utc).astimezone(ZoneInfo("America/Santiago")).isoformat()
    user_id = str(uuid.uuid4())
    token = create_token(user_id)
    hashed_pwd = hash_password(user.password)

    user_dict = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "password": hashed_pwd,
        "phones": [phone.dict() for phone in user.phones],
        "created": now,
        "modified": now,
        "last_login": now,
        "token": token,
        "isactive": True
    }

    user_collection.insert_one(user_dict)

    user_dict.pop("password")  # No enviar password en respuesta
    return user_dict