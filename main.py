from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from database import get_db
from auth import get_current_user
from schema import UserCreate, UserOut
from auth import router as auth_router
from routes.admin_routes import router as admin_router
from routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Movie Ticket Booking System", version="1.0.0")

app.include_router(admin_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Ticket Booking System API"}