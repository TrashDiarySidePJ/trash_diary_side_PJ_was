from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
  email: EmailStr
  password: str
  nickname: str
  
class LoginRequest(BaseModel):
  email: EmailStr
  password: str
  
class RefreshRequest(BaseModel):
  refresh_token: str
  
class TokenResponse(BaseModel):
  access_token: str
  refresh_token: str