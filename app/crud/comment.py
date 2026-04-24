from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

async def get_comments_by_post(db: AsyncSession, post_id: int) -> List[Comment]:
    stmt = select(Comment).options(selectinload(Comment.author)).where(Comment.post_id == post_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_comment(db: AsyncSession, comment: CommentCreate, author_id: int) -> Comment:
    db_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        author_id=author_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    
    stmt = select(Comment).options(selectinload(Comment.author)).where(Comment.id == db_comment.id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def delete_comment(db: AsyncSession, comment_id: int) -> bool:
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(stmt)
    db_comment = result.scalars().first()
    
    if db_comment:
        await db.delete(db_comment)
        await db.commit()
        return True
    return False

async def get_comment(db: AsyncSession, comment_id: int) -> Optional[Comment]:
     stmt = select(Comment).where(Comment.id == comment_id)
     result = await db.execute(stmt)
     return result.scalars().first()
