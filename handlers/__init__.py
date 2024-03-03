from handlers.tasks import router as task_router
from handlers.ping import router as ping_router

routers = [task_router, ping_router]
