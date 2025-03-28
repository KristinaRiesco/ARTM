from backend.models.user import User
from backend.core.extensions import db, bcrypt
from sqlalchemy.exc import IntegrityError


def register_user(username, email, password):
    if not username or not email or not password:
        return {"error": "All fields are required to register"}

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=password_hash)

    try:
        db.session.add(new_user)
        db.session.commit()
        return{"message":"User registered successfully"}
    except IntegrityError:
        db.session.rollback()
        return {"error": "Username or email already exists"}

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return {"message":"Login Successful", "user_id": user.id, "username": user.username}
    else:
        return {"error": "Invalid credentials. Email or password is not correct"}

def get_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error":"User not found"}
    return {"username": user.username, "email": user.email}

def update_profile(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]

    db.session.commit()
    return {"message":"Profile updated successfully"}