from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class ConnectionRequest(db.Model):

    __tablename__ = "connection_requests"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    ) 

class UserProfile(db.Model):

    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False)

    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    city = db.Column(db.String(100))
    teach_skill = db.Column(db.String(100))
    learn_skill = db.Column(db.String(100))
    proficiency_level = db.Column(db.String(50))
    preferred_language = db.Column(db.String(50))
    learning_mode = db.Column(db.String(50))
    availability = db.Column(db.String(50))
    rating = db.Column(db.Float, default=0.0)
    completed_exchanges = db.Column(db.Integer, default=0)    