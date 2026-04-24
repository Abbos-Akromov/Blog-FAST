from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.user import UserResponse

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    slug: str
    
    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = False
    category_id: int | None = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_published: bool | None = None
    category_id: int | None = None

class PostResponse(PostBase):
    id: int
    slug: str
    created_at: datetime
    author_id: int
    
    author: UserResponse | None = None
    category: CategoryResponse | None = None
    
    model_config = ConfigDict(from_attributes=True)
