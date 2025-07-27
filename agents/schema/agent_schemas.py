from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class FlightBase(BaseModel):
    flight_number: str
    airline: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    seats_available: int
    cabin_class: str
    status: str = "scheduled"

class FlightCreate(FlightBase):
    pass

class Flight(FlightBase):
    id: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class HotelBase(BaseModel):
    name: str
    address: Address
    star_rating: int
    room_type: str
    price_per_night: float
    available_rooms: int
    check_in_date: datetime
    check_out_date: datetime
    amenities: List[str]

class HotelCreate(HotelBase):
    pass

class Hotel(HotelBase):
    id: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class BookingBase(BaseModel):
    user_id: str
    total_price: float
    booking_date: datetime
    status: str = "confirmed"

class FlightBookingCreate(BookingBase):
    flight_id: str
    passenger_name: str
    passenger_email: str
    seat_number: Optional[str] = None

class HotelBookingCreate(BookingBase):
    hotel_id: str
    guest_name: str
    guest_email: str
    room_number: Optional[str] = None

class FlightBooking(BookingBase):
    id: str
    flight_id: str
    passenger_name: str
    passenger_email: str
    seat_number: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class HotelBooking(BookingBase):
    id: str
    hotel_id: str
    guest_name: str
    guest_email: str
    room_number: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}