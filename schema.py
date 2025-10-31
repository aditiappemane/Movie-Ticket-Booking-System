from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    
    email: str
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" 

class TheaterBase(BaseModel):
    name: str
    address: Optional[str] = None

class TheaterCreate(TheaterBase):
    pass

class ScreenCreate(BaseModel):
   pass

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    duration: int  # duration in minutes
 
class seatCreate(BaseModel):
    label: str

class ShowCreate(BaseModel):
    movie_id: int
    screen_id: int
    start_time: datetime
    price: float

class BookingCreate(BaseModel):
    show_id: int
    seat_ids: List[int]
