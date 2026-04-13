from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.auth import hash_password, verify_password, create_token
from pydantic import BaseModel
from typing import List
from datetime import datetime

# Rota para usuários
router = APIRouter(prefix="/users", tags=["Users"])

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

# Rota para criar um usuário novo
@router.post("/", response_model=UserResponse)
def criar_usuario(data: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id, name, email, role, created_at",
        (data["name"], data["email"], hash_password(data["password"]), data.get("role", "client"))
    )
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(user)

# Rota para listar todos os usuários
@router.get("/usuarios", response_model=List[UserResponse])
def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, role, created_at FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(u) for u in users]