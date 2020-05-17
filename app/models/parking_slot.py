"""
Parking slot is a single space where a vehicle can be parked
"""
from app import db


class ParkingSlot(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    parking_area_id = db.Column(db.Integer, db.ForeignKey('parking_area.id'), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)
