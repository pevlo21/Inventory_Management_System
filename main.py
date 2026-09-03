from fastapi import FastAPI

from api.route import v1_router
from db.sqlite import create_db

app=FastAPI()

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(v1_router)