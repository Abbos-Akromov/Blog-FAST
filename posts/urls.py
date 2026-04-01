from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix='/posts', tags=['Posts'])

posts_db = [
    {"id": 1, "title": "FastAPI nima?", "body": "FastAPI — zamonaviy framework...", "author": "admin", "published": True, "likes": 15},
    {"id": 2, "title": "Python o'rganish", "body": "Qanday boshlash...", "author": "user1", "published": True, "likes": 8},
    {"id": 3, "title": "Draft", "body": "Tugallanmagan...", "author": "admin", "published": False, "likes": 0},
]

class PostCreate(BaseModel):
    title: str
    body: str
    author: str

@router.get('/')
async def posts_list(author: Optional[str] = None, published: bool = True):
    result = [p for p in posts_db if p['published'] == published]
    if author:
        result = [p for p in result if p['author'] == author]
    return {'posts': result, 'total': len(result)}

@router.get('/{post_id}')
async def post_detail(post_id: int):
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail='Post topilmadi')
    return post

@router.post('/create')
async def post_create(data: PostCreate):
    new_post = {'id': len(posts_db) + 1, **data.dict(), 'published': False, 'likes': 0}
    posts_db.append(new_post)
    return {'message': 'Post yaratildi (draft)', 'post': new_post}

@router.post('/{post_id}/publish')
async def post_publish(post_id: int):
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail='Post topilmadi')
    if post['published']:
        raise HTTPException(status_code=400, detail='Allaqachon nashr qilingan')
    post['published'] = True
    return {'message': 'Nashr qilindi'}

@router.post('/{post_id}/like')
async def post_like(post_id: int):
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail='Post topilmadi')
    post['likes'] += 1
    return {'total_likes': post['likes']}