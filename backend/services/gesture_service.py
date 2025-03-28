#need to fill with gesture routes
from backend.models.gestures import Gesture
from backend.core.extensions import db, bcrypt
from sqlalchemy.exc import IntegrityError



# backend/services/gesture_service.py

def perform_action(gesture: str) -> dict:
    if not gesture:
        return {"status": "error", "message": "No gesture provided"}

    # Define gesture → action mapping
    gesture_actions = {
        "peace_sign": {"action": "open_url", "data": "https://www.google.com"},
        "thumbs_up": {"action": "notify", "data": "thumbs up!"},
        "index_up": {"action": "notify", "data": "index finger up!"},
        "rock_and_roll_salute": {"action": "notify", "data": "rock and roll!"},
        "fist": {"action": "notify", "data": "fists up!"},
        "l_sign": {"action": "notify", "data": "L Sign!"}
    }

    action = gesture_actions.get(gesture, {"action": "none", "data": "No action available"})
    return {"status": "success", "action": action}
