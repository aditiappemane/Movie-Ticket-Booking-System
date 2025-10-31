from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Booking, User
from database import get_db
from auth import get_current_user
from schema import UserCreate, UserOut
from auth import get_password_hash



router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/movies")
def read_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.get("/shows")
def read_shows(db: Session = Depends(get_db)):
    return db.query(Show).all()

@ROUTER.get(showa="/shows/{show_id}/seats")
def read_available_seats(show_id: int, db: Session = Depends(get_db)):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    booked_seats = db.query(Booking).filter(Booking.show_id == show_id).all()
    booked_seat_numbers = set()
    for booking in booked_seats:
        booked_seat_numbers.update(booking.seat_numbers.split(","))
    screen = db.query(Screen).filter(Screen.id == show.screen_id).first()
    all_seat_numbers = {str(i) for i in range(1, screen.capacity + 1)}
    available_seat_numbers = all_seat_numbers - booked_seat_numbers
    return {"available_seats": list(available_seat_numbers)}

@router.post("/bookings")
def create_booking(booking_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_booking = Booking(
        user_id=current_user.id,
        show_id=booking_data["show_id"],
        seat_numbers=",".join(booking_data["seat_numbers"]),
        booking_time=datetime.utcnow()
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/bookings")
def read_user_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings

@router.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"detail": "Booking cancelled successfully"}    