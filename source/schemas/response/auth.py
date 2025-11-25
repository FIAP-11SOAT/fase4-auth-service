from pydantic import BaseModel


class AuthResponse(BaseModel):
    token: str
    user_id: str
    name: str
    email: str


class RegisterResponse(BaseModel):
    user_id: str
    tax_id: str
    email: str
    name: str
    message: str = "User registered successfully"
