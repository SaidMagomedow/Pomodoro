from contextlib import asynccontextmanager

from app.dependecy import get_tasks_repository
from app.tasks.repository.task import TaskRepository
from fastapi import FastAPI, Depends

from app.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # broker_consumer = await get_broker_consumer()
    # await broker_consumer.consume_callback_message()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/app/ping")
async def ping_app():
    return {"text": "app is working"}


@app.get("/db/ping")
async def ping_db(task_repository: TaskRepository = Depends(get_tasks_repository)):
    await task_repository.ping_db()
