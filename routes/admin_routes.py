from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Booking, User 
from database import get_db
from auth import get_current_user
from schema import UserCreate, UserOut, TheaterCreate, TheaterOut, ScreenCreate, ScreenOut, MovieCreate, MovieOut
from auth import get_password_hash ,require_role

router = APIRouter(prefix="/admin", tags=["admin"])
get_admin=require_role("admin")

#theater

@router.post("/theatres")
def create_theater(theater: TheaterCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    new_theater = Theater(**theater.dict())
    db.add(new_theater)
    db.commit()
    db.refresh(new_theater)
    return new_theater  

@router.post("/theatres/{theater_id}/screens")
def create_screen(theater_id: int, screen: ScreenCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    new_screen = Screen(theater_id=theater_id, **screen.dict())
    db.add(new_screen)
    db.commit()
    db.refresh(new_screen)
    return new_screen

#screen

@router.post("/screens/{screen_id}/seats")
def create_seats(screen_id: int, seat: seatCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    new_seat = Seat(screen_id=screen_id, **seat.dict())
    db.add(new_seat)
    db.commit()
    db.refresh(new_seat)
    return new_seat 

#movie
@router.post("/movies")
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie    
#show
@router.post("/shows")
def create_show(show: ShowCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    new_show = Show(**show.dict())
    db.add(new_show)
    db.commit()
    db.refresh(new_show)
    return new_show

#view all bookings
@router.get("/bookings")
def get_all_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    bookings = db.query(Booking).all()
    return bookings
