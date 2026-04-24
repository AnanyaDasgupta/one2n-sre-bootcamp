from fastapi import FastAPI

from app.routes.system_routes import router as system_router


app = FastAPI()
app.include_router(system_router)
