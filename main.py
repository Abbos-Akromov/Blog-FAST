from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full Asynchronous Blog Site with Users, Posts, and Comments",
    version="1.0.0",
    docs_url="/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get('/')
async def index():
    return {
        'message': f'{settings.PROJECT_NAME} ishga tushdi',
        'docs': '/docs',
        'api_v1': settings.API_V1_STR
    }
