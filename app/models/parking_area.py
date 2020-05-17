"""
Parking area is a space which contains one or more parking slots
"""
from app import db


class ParkingArea(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    image = db.Column(db.String(512), nullable=True)

