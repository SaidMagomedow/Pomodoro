from fastapi import FastAPI
from handlers import routers

app = FastAPI()


for router in routers:
    app.include_router(router)
