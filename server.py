"""Server for swolemates app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify, url_for
from model import connect_to_db, db, Location, User, Save
from authlib.integrations.flask_client import OAuth
import os
import bcrypt
from yelp.client import Client
MY_API_KEY = "Bearer mUOoEuwbg4In0FAGUm041a9Std20NoqFWNgw1i36aP8pnVuFYFn5RcKqTcamjM21niuNO9oYfjGexB2zOxGlgGBy8Vd1KfqOXKi6b2SvU2Coy5hzIprEWYW3OgreYXYx"
import requests
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# oauth = OAuth(app)
# google = oauth.register(
# name="google",
# client_id="1095412791174-qtvreoopct68oqaa0d5vr51a6h70753i.apps.googleusercontent.com",
# client_secret=os.environ["CLIENT_SECRET"],
# access_token_url="https://accounts.google.com/o/oauth2/token",
# access_token_params=None,
# authorize_url="https://accounts.google.com/o/oauth2/auth",
# authorize_params=None,
# api_base_url="https://www.googleapis.com/oauth2/v1/",
# client_kwargs={"scope": "openid profile email"}
# )

# @app.route("/google-login")
# def login():
#     google = oauth.create_client("google")
#     redirect_uri = url_for("authorize", _external=True)
#     return google.authorize_redirect(redirect_uri)

# @app.route("/authorize")
# def authorize():
#     google = oauth.create_client("google")
#     token = google.authorize_access_token()
#     print("\n", "*"*20, token,"\n")
#     resp = google.get("userinfo")
#     resp.raise_for_status()
#     profile = resp.json()
#     print("\n", "*"*20, profile,"\n")
#     if crud.get_user_by_email(profile["email"]):
#         user = crud.get_user_by_email(profile["email"])
#         session["user_id"] = user.user_id
#     else:
#         hashed_password = bcrypt.hashpw(profile['id'].encode('utf8'), bcrypt.gensalt())
#         username = profile["given_name"]
#         crud.create_user(profile["email"], hashed_password, username)
#         user = crud.get_user_by_email(profile["email"])
#         session["user_id"] = user.user_id
#     return redirect("/")

url = "https://api.yelp.com/v3/businesses/search"
headers = {"Authorization": "Bearer mUOoEuwbg4In0FAGUm041a9Std20NoqFWNgw1i36aP8pnVuFYFn5RcKqTcamjM21niuNO9oYfjGexB2zOxGlgGBy8Vd1KfqOXKi6b2SvU2Coy5hzIprEWYW3OgreYXYx" }
params = {"term": "gyms", "location": "Sunnyvale", "limit": 50, "radius": 50}
results = requests.get(url, params=params, headers=headers)
results_dict = results.json()
businesses = results_dict["businesses"]

@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")
    
@app.route("/login")
def show_login():
    """Show login form."""
    if "user_id" not in session:
        return render_template("login.html")
    else:
        flash("You are already logged in.")
        return redirect("/my_profile")

@app.route("/login", methods=["POST"])
def login_user():
    """Login existing users"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    print(user)
    if user:
        if user.email == email and user.password == password:
            print(user.email, email)
            session["user_id"] = user.user_id
            session["user_email"] = user.email
            session["fname"] = user.fname
            flash(f"Welcome back, {user.email}!")
            return redirect("/my_profile")
        else:
            flash("Incorrect password. Please try again")
    else:
        flash("Email not registered. Please register first or check that you entered your email correctly.")
    return redirect("/login")


@app.route("/logout")
def logout():
    """Logout User and End Session"""
    if "user_id" in session:
        del session["user_id"]
        flash("Logged out. Thanks for visiting.")
        return render_template("logout.html")
    else: 
        return redirect("/")

@app.route("/my_profile")
def to_user_profile():
    """For user to view their profile"""
    user = crud.get_user_by_email(session.get("user_email")) 
    if "user_id" in session:
        return render_template("my_profile.html", user=user)
    else:
        flash("You must be logged in to see your profile.")
        return redirect("/")


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_buddies.html", users=users)


@app.route("/create-user", methods=["POST"])
def create_user():
    """Create new user account"""
    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    gender = request.form.get("gender")
    user = crud.get_user_by_email(email)
    if user:
        flash("That email is already associated with an account.")
    else:
        crud.create_user(email, password, fname, lname, gender)
        flash("Account created! Please log in.")
    
    return redirect("/login")

@app.route("/search")
def search(search_term="gyms", location="San Jose"):
    search_term = request.args.get("term")
    location = request.args.get("location")
    params = {"term": search_term, "location": location}
    results = requests.get(url, params=params, headers=headers)
    results_dict = results.json()
    businesses = results_dict["businesses"]
    print(businesses)
    return render_template("location_results.html", businesses=businesses)

@app.route("/fav_location.json", methods=["POST"])
def fav_location():
    """Add a user"s preferred location to their user profile."""
    location_id = request.json.get("location_id")
    name = request.json.get("location_name")
    user_id = request.json.get("user_id")
    location = crud.get_location_by_id(location_id)
    if location is None:
        crud.create_location(location_id=location_id, name=name)
        crud.save_user_location(location_id=location_id, user_id=user_id)
        return jsonify({ "success": True, "status": "Your location has been saved"})
    else:
        crud.save_user_location(location_id=location_id, user_id=user_id)
        return jsonify({ "success": True, "status": "Your location has been saved"})


@app.route("/users_by_gym/<location_id>")
def members(location_id): 
    """See the users who also favorited that gym"""
    gym_users = crud.get_users_by_gym(location_id)
    print("this is *********", gym_users)
    return render_template("gym_users.html", gym_users=gym_users)

@app.route("/save_buddy.json", methods=["POST"])
def save_buddy():
    """Save another user as a buddy"""
    buddy_id = request.json.get("buddy_id")
    buddy = crud.get_user_by_id(buddy_id)
    user_id = request.json.get("user_id")
    user = crud.get_user_by_id(user_id)
    already_saved = crud.check_save(buddy_id=buddy_id, user_id=user_id)
    if already_saved:
        return jsonify({ "fail": False, "status": "You already saved that buddy"})
    else: 
        crud.create_buddy(buddy=buddy, user=user) 
        return jsonify({ "success": True, "status": "Your buddy has been saved"})
    
@app.route("/unsave_buddy.json", methods=["POST"])
def unsave_buddy():
    """Unsave a buddy"""
    buddy_id = request.json.get("buddy_id")
    user_id = request.json.get("user_id")
    already_saved = crud.check_save(buddy_id=buddy_id, user_id=user_id)
    if not already_saved:
        return jsonify({ "fail": False, "status": "You already removed that buddy"})
    else: 
        crud.unsave(buddy_id=buddy_id, user_id=user_id) 
        return jsonify({ "success": True, "status": "Your buddy has been removed"})
    
@app.route("/buddies")
def view_buddies():
    """View user"s buddies"""
    all_buddies= crud.get_user_buddies(session["user_id"])
    print("*******************************", all_buddies)
    return render_template("buddies.html", all_buddies=all_buddies)

@app.route("/messages")
def view_messages():
    """View user"s messages they received"""
    messages= crud.view_messages(session["user_id"])
    return render_template("messages.html", messages=messages)

@app.route("/sent-messages")
def view_sent_messages():
    """View user"s messages they sent"""
    messages= crud.view_sent_messages(session["user_id"])
    return render_template("sent_messages.html", messages=messages)

@app.route("/send_message.json", methods=["POST"])
def send_message():
    """Send a saved buddy a message"""
    buddy_id = request.json.get("buddy_id")
    buddy = crud.get_user_by_id(buddy_id)
    user_id = request.json.get("user_id")
    user = crud.get_user_by_id(user_id)
    message = request.json.get("message_content")
    crud.create_message(buddy=buddy, user=user, message=message) 
    return jsonify({ "success": True, "status": "Your message was sent!"})
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

