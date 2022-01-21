"""CRUD operations."""

from model import  connect_to_db, db, Location, User, Save
################ USER FUNCTIONS ##########################

def create_user(email, password, fname=None, lname=None, gender=None, pronouns=None, 
                about_me=None, fav_location=None):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, gender=gender, pronouns=pronouns, 
                about_me=about_me, email=email, password=password, fav_location=fav_location)

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

def get_users_by_gym(location_id):
    """Return a user by email."""

    return User.query.filter(User.fav_location == location_id).all()

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

def save_user_location(location_id, user_id):
    """Save a location as a favorite to an user profile""" #change this to implement logic for if user wants to change location
    location_object = Location.query.get(location_id)
    if location_object is None: 
        location_object = Location(location_id=location_id)
    user = User.query.get(user_id)
    user.location = location_object # user objects have a relationship called location
    db.session.add(user) # because user and location_obj are related, this db.session.add actually adds them both
    db.session.commit()
  
############ SAVE FUNCTIONS ################

def create_buddy(buddy, user):
    """Allow user to save a buddy."""
    save = Save(buddy=buddy, user=user)
    db.session.add(save)
    db.session.commit()
    return save

def check_save(buddy_id, user_id):
    return Save.query.filter(Save.buddy_id==buddy_id).filter(Save.user_id==user_id).first()
        

def unsave(buddy_id, user_id):
    """Unsave an user as a buddy."""
    
    unsave = Save.query.filter(Save.buddy_id==buddy_id).filter(Save.user_id==user_id).first()
    if unsave:
        db.session.delete(unsave)
        db.session.commit()

    return "function complete"
    

def get_all_saves_by_user(user_id):
    """List of all the saves for each user."""
    return Save.query.filter_by(user_id=user_id).all()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
