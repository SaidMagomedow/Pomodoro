from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumer import make_aqmp_consumer
from app.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_aqmp_consumer()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(user_router)
