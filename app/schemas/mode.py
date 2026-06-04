from pydantic import BaseModel

class ModeResponse(BaseModel):
  mode_id: int
  mode_name: str