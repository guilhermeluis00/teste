from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.auth import verify_password, create_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginInput(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginInput):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (data.email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    token = create_token(user["id"], user["email"])
    return {"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}}