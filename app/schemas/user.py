from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
  user_id: int
  email: EmailStr
  nickname: str