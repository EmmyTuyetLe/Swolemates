"""CRUD operations."""

from model import db, Location, User, Save, connect_to_db

################ USER FUNCTIONS ##########################

def create_user(email, password, fname=None, lname=None, gender=None, pronouns=None, 
                about_me=None, fav_location=None):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, gender=gender, pronouns=pronouns, 
                about_me=about_me, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by user id."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

############ LOCATION FUNCTIONS ##############################

def create_location(location_id,name):
    """Create and return a new location."""

    location = Location(location_id=location_id, name=name)

    db.session.add(location)
    db.session.commit()

    return location


def get_locations():
    """Return all locations."""

    return Location.query.all()


def get_location_by_id(location_id):
    """Return a location by primary key."""

    return Location.query.get(location_id)

def save_location(location_id, user_id):
    """Save a location as a favorite to an user profile"""
    User.query.filter_by(user_id=user_id).update(
        {"fav_location": location_id  
        }
    )
    db.session.commit()
  
############ SAVE FUNCTIONS ################

def create_buddy(buddy, user):
    """Allow user to save a buddy."""

    save = Save(buddy=buddy, user=user)

    db.session.add(save)
    db.session.commit()

    return save



if __name__ == "__main__":
    from server import app

    connect_to_db(app)
