from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.crud import post as crud_post
from app.schemas.post import PostCreate, PostUpdate, PostResponse, CategoryCreate, CategoryResponse

router = APIRouter()

# Categories
@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    category_in: CategoryCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Only active users can create categories for now
    category = await crud_post.get_category_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return await crud_post.create_category(db, category=category_in)

@router.get("/categories", response_model=List[CategoryResponse])
async def read_categories(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud_post.get_categories(db)

# Posts
@router.post("/", response_model=PostResponse)
async def create_post(
    post_in: PostCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud_post.create_post(db, post=post_in, author_id=current_user.id)

@router.get("/", response_model=List[PostResponse])
async def read_posts(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100
):
    return await crud_post.get_posts(db, skip=skip, limit=limit)

@router.get("/{slug}", response_model=PostResponse)
async def read_post(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    post = await crud_post.get_post_by_slug(db, slug=slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/{slug}", response_model=PostResponse)
async def update_post(
    slug: str,
    post_in: PostUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_post = await crud_post.get_post_by_slug(db, slug=slug)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await crud_post.update_post(db, db_post=db_post, post_update=post_in)

@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    slug: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_post = await crud_post.get_post_by_slug(db, slug=slug)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await crud_post.delete_post(db, db_post=db_post)
    return None
