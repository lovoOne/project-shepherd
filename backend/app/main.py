from fastapi import FastAPI

from app.core.config import settings
from app.api.v1 import councils
from app.api.v1 import churches
from app.api.v1 import members
from app.api.v1 import users
from app.api.v1 import auth
from app.api.v1 import dashboard

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)


app.include_router(
    councils.router,
    prefix="/api/v1"
)

app.include_router(
    churches.router,
    prefix="/api/v1",
)

app.include_router(
    members.router,
    prefix="/api/v1",
)

app.include_router(
    dashboard.router,
    prefix="/api/v1",
)

app.include_router(
    users.router,
    prefix="/api/v1",
)

app.include_router(
    auth.router,
    prefix="/api/v1",
)

@app.get("/")
def root():
    return {
        "message": f"Bienvenido a {settings.APP_NAME}"
    }
    
    