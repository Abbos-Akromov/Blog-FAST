from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.user import UserResponse

class CommentBase(BaseModel):
    content: str
    post_id: int

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    author: UserResponse | None = None
    
    model_config = ConfigDict(from_attributes=True)
