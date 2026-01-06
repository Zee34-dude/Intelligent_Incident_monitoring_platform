from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, authentication, service, organization
from app.health.runner import health_check_loop

# Create tables first
models.Base.metadata.create_all(bind=engine)

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(health_check_loop())
    yield
    task.cancel()

# FastAPI app
app = FastAPI(lifespan=lifespan)

# Routers
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(service.router)
app.include_router(organization.router)
