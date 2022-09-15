import uvicorn
from fastapi import FastAPI

from app.db.database import Base, engine
from app.api.api import api_router


app = FastAPI()
app.include_router(api_router, prefix="/api")

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)



