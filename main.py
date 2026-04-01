from fastapi import FastAPI
from posts.urls import router as posts_router
from comments.urls import router as comments_router

app = FastAPI(title="Blog Site")
app.include_router(router=posts_router)
app.include_router(router=comments_router)

@app.get('/')
async def index():
    return {'message': 'Blog Site API'}