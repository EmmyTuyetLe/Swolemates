"""Models for swolemates app"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Location(db.Model):
    """A location that users can save."""

    __tablename__ = "locations"

    location_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f"<Location location_id={self.location_id} location_name={self.location_name}>"


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    gender = db.Column(db.String)
    pronouns = db.Column(db.String)
    about_me = db.Column(db.Text)
    fav_location = db.Column(db.String, db.ForeignKey("locations.location_id"))
    
    location = db.relationship("Location", backref="users")

    def __repr__(self):
        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname}>"


class Save(db.Model):
    """User profiles that have been saved."""

    __tablename__ = "saves"

    save_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    buddy_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) #field for user who is being saved
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) #field for current user saving

    buddy = db.relationship("User", backref="user", foreign_keys=[buddy_id])
    user = db.relationship("User", backref="buddies", foreign_keys=[user_id])

    def __repr__(self):
        return f"<Save save_id={self.save_id} buddy_id={self.buddy_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///swolemates", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    users = User.query.all()

