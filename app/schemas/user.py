from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
  user_id: int
  email: EmailStr
  name: str
  nickname: str
  phone: str
  mode_id: int