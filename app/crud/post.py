from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from slugify import slugify

from app.models.post import Post, Category
from app.schemas.post import PostCreate, PostUpdate, CategoryCreate

# Category CRUD
async def get_category_by_name(db: AsyncSession, name: str) -> Optional[Category]:
    stmt = select(Category).where(Category.name == name)
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_category(db: AsyncSession, category: CategoryCreate) -> Category:
    db_category = Category(
        name=category.name,
        slug=slugify(category.name)
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_categories(db: AsyncSession) -> List[Category]:
    stmt = select(Category)
    result = await db.execute(stmt)
    return result.scalars().all()

# Post CRUD
async def get_post_by_slug(db: AsyncSession, slug: str) -> Optional[Post]:
    stmt = select(Post).options(selectinload(Post.author), selectinload(Post.category)).where(Post.slug == slug)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Post]:
    stmt = select(Post).options(selectinload(Post.author), selectinload(Post.category)).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_post(db: AsyncSession, post: PostCreate, author_id: int) -> Post:
    base_slug = slugify(post.title)
    
    # Simple logic to handle duplicate slugs (can be improved)
    stmt = select(Post).where(Post.slug == base_slug)
    result = await db.execute(stmt)
    existing = result.scalars().first()
    slug = base_slug if not existing else f"{base_slug}-{author_id}"
    
    db_post = Post(
        title=post.title,
        slug=slug,
        content=post.content,
        is_published=post.is_published,
        category_id=post.category_id,
        author_id=author_id
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    
    # Eagerly load relationships so they can be returned
    return await get_post_by_slug(db, slug=db_post.slug)

async def update_post(db: AsyncSession, db_post: Post, post_update: PostUpdate) -> Post:
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    
    await db.commit()
    await db.refresh(db_post)
    return await get_post_by_slug(db, slug=db_post.slug)

async def delete_post(db: AsyncSession, db_post: Post):
    await db.delete(db_post)
    await db.commit()
