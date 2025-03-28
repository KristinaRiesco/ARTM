from backend.core.extensions import db
from sqlalchemy import Column, Text, Integer, String, TIMESTAMP, ForeignKey
from datetime import datetime

class Gesture(db.Model):
    __tablename__ = "gestures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    gesture_name = Column(String(100), nullable=False)
    gesture_data = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"<Gesture (gesture_name={self.gesture_name}, user_id={self.user_id})>"