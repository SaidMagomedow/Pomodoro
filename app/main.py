from fastapi import FastAPI
from app.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router

app = FastAPI()

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(user_router)
