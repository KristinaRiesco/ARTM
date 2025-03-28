# backend/core/database.py

from backend.core.extensions import db
from backend.core.config import Config  # contains DB URI
from backend.models.user import User
from backend.models.gestures import Gesture
from flask import Flask

def init_db():
    # Use a temporary Flask app just to initialize SQLAlchemy
    db.create_all()
    print("Database initialized")

