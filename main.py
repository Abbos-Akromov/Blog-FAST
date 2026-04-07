from fastapi import FastAPI
from database import engine, Base
from posts.urls import router as posts_router
from users.urls import router as users_router
from posts.models import Category, Post

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog Site API",
    description="Vazifa: 4 ta loyihadan biri - Blog Sayti",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(posts_router)

@app.get('/')
async def index():
    return {
        'message': 'Blog Site API ishga tushdi',
        'docs': '/docs'
    }
