from fastapi import FastAPI
from api.routes import router
from core.database import engine
from core.models import Base

app = FastAPI(title="Kasparro Backend & ETL System")

# Create tables at startup (safe for demo)
Base.metadata.create_all(bind=engine)

app.include_router(router)
