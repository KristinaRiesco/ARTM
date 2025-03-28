from backend.core.extensions import db
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"