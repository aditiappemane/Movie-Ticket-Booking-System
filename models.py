from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from database import Base   
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="user")  # roles: user, admin

    
    bookings = relationship("Booking", back_populates="user")

class theater(Base):
    __tablename__ = "theaters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    screens = relationship("Screen", back_populates="theater")

class Screen(Base):
    __tablename__ = "screens"
    
    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    screen_number = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    name= Column(String, nullable=False)
    address= Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    
    # theater = relationship("theater", back_populates="screens")
    Screen=relationship("Screen", back_populates="theater")


    class Movie(Base):
        __tablename__ = "movies"
        
        id = Column(Integer, primary_key=True, index=True)
        title = Column(String, nullable=False)
        description = Column(String)
        duration = Column(Integer)  # duration in minutes
        genre = Column(String)
        director = Column(String)
        release_date = Column(String)
        
        show = relationship("Show", back_populates="movie")

class Show(Base):
    __tablename__ = "shows"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    show_time = Column(String, nullable=False)
    
    movie = relationship("Movie", back_populates="shows")
    screen = relationship("Screen", back_populates="shows")
    bookings = relationship("Booking", back_populates="show")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    seats_booked = Column(Integer, nullable=False)
    booking_time = Column(String, default=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    status = Column(String, default="confirmed") 
     # statuses: confirmed, cancelled
    user = relationship("User", back_populates="bookings")
    seats=relationship("Show", back_populates="bookings")

class BookingSeat(Base):
    __tablename__ = "booking_seats"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    seat_number = Column(String, nullable=False)
    
    booking = relationship("Booking", back_populates="seats")
    show = relationship("Show", back_populates="bookings")
