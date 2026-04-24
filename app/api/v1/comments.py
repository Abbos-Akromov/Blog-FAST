from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.crud import comment as crud_comment
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter()

@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment_in: CommentCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud_comment.create_comment(db, comment=comment_in, author_id=current_user.id)

@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def read_comments(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud_comment.get_comments_by_post(db, post_id=post_id)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    comment = await crud_comment.get_comment(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await crud_comment.delete_comment(db, comment_id=comment_id)
    return None
