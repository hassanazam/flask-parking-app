"""
Booking table, which maintain the history of booking and cancellation requests made by users
"""

from app import db


class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    parking_slot_id = db.Column(db.Integer, db.ForeignKey('parking_slot.id'), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)  # epoch format
    end_time = db.Column(db.Integer, nullable=False)    # epoch format
    status = db.Column(db.String(32), nullable=False)   # Could be booked OR cancelled
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


