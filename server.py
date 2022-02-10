"""Server for swolemates app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify, url_for
from model import connect_to_db, db, Location, User, Save
from authlib.integrations.flask_client import OAuth
import os
import bcrypt
from yelp.client import Client
from twilio.rest import Client
MY_API_KEY = os.environ["API_KEY"]
client = Client(MY_API_KEY)
import requests
import crud
from twilio.twiml.messaging_response import MessagingResponse
from jinja2 import StrictUndefined
import werkzeug

app = Flask(__name__)
app.secret_key = "dev ***************************"
app.jinja_env.undefined = StrictUndefined

#GOOGLE OAuth setup
oauth = OAuth(app)
google = oauth.register(
name="google",
client_id=os.environ["CLIENT_ID"],
client_secret=os.environ["CLIENT_SECRET"],
access_token_url="https://accounts.google.com/o/oauth2/token",
access_token_params=None,
authorize_url="https://accounts.google.com/o/oauth2/auth",
authorize_params=None,
api_base_url="https://www.googleapis.com/oauth2/v1/",
client_kwargs={"scope": "openid profile email"}
)

@app.route("/google-login")
def login():
    google = oauth.create_client("google")
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    resp.raise_for_status()
    profile = resp.json()
    if crud.get_user_by_email(profile["email"]):
        user = crud.get_user_by_email(profile["email"])
        session["user_id"] = user.user_id
    else:
        password = bcrypt.hashpw(profile["id"].encode("utf8"), bcrypt.gensalt())
        crud.create_user(profile["email"], password)
        user = crud.get_user_by_email(profile["email"])
        session["user_id"] = user.user_id
    return redirect("/my_profile")


# #Yelp API setup
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
    if user:
        if werkzeug.security.check_password_hash(user.password, password):
            if user.email == email:
                session["user_id"] = user.user_id
                session["user_email"] = user.email
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
        flash("You're already logged out.")
        return redirect("/")

@app.route("/my_profile")
def to_user_profile():
    """For user to view their profile"""
    if "user_id" in session:
        user_id = session["user_id"]
        user = crud.get_user_by_id(user_id)
        location =  crud.get_location_by_id(user.fav_location)
        return render_template("my_profile.html", user=user, location=location)
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
    phone = request.form.get("gender")
    user = crud.get_user_by_email(email)
    if user:
        flash("That email is already associated with an account.")
    else:
        hashed_password = werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=10)
        crud.create_user(email, hashed_password, fname, lname, gender, phone)
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
    return render_template("location_results.html", businesses=businesses)

@app.route("/fav_location.json", methods=["POST"])
def fav_location():
    """Add a user"s preferred location to their user profile."""
    location_id = request.json.get("location_id")
    name = request.json.get("location_name")
    user_id = request.json.get("user_id")
    # url = request.json.get("location_url")
    location = crud.get_location_by_id(location_id)
    if location is None:
        crud.create_location(location_id=location_id, name=name, url=url)
        crud.save_user_location(location_id=location_id, user_id=user_id)
        return jsonify({ "success": True, "status": "Your favorite location has been saved"})
    else:
        crud.save_user_location(location_id=location_id, user_id=user_id)
        return jsonify({ "success": True, "status": "Your favorite location has been saved"})


@app.route("/users_by_gym/<location_id>")
def members(location_id): 
    """See the users who also favorited that gym"""
    gym_users = crud.get_users_by_gym(location_id)
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
    if already_saved:
        crud.unsave(buddy_id=buddy_id, user_id=user_id) 
        return jsonify({ "success": True, "status": "Your buddy has been removed"})
    else: 
        return jsonify({ "fail": False, "status": "That buddy has already been removed"})
    
@app.route("/buddies")
def view_buddies():
    """View user"s buddies"""
    all_buddies= crud.get_user_buddies(session["user_id"])
    return render_template("buddies.html", all_buddies=all_buddies)

@app.route("/messages")
def view_messages():
    """View user"s messages they received"""
    if "user_id" in session:
        messages= crud.view_messages(session["user_id"])
        return render_template("messages.html", messages=messages)
    else:
        flash("You must be logged in to read your messages.")
        return redirect("/")

@app.route("/sent-messages")
def view_sent_messages():
    """View user"s messages they sent"""
    if "user_id" in session:
        messages= crud.view_sent_messages(session["user_id"])
        return render_template("sent_messages.html", messages=messages)
    else:
        flash("You must be logged in to read your sent messages.")
        return redirect("/")

@app.route("/send_message.json", methods=["POST"])
def send_message():
    """Send a saved buddy a message"""
    buddy_id = request.json.get("buddy_id")
    buddy = crud.get_user_by_id(buddy_id)
    user_id = request.json.get("user_id")
    user = crud.get_user_by_id(user_id)
    message = request.json.get("message_content")
    crud.create_message(buddy=buddy, user=user, message=message)
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    send_num = os.environ['TWILIO_PHONE']
    client = Client(account_sid, auth_token)
    new_message = client.messages.create(
                                from_= send_num,
                                body=f'Hello {buddy.fname} you received a message from {user.fname} {user.lname[0]} that says "{message}"',
                                to=f'+1'+buddy.phone
                            )
    return jsonify({ "success": True, "status": "Your message was sent!"})
    
@app.route("/reply_message.json", methods=["POST"])
def reply_message():
    """Send a saved buddy a message"""
    buddy_id = request.json.get("buddy_id")
    buddy = crud.get_user_by_id(buddy_id)
    user_id = request.json.get("user_id")
    user = crud.get_user_by_id(user_id)
    message = request.json.get("message_content")
    crud.create_message(buddy=buddy, user=user, message=message)
    return jsonify({ "success": True, "status": f"Your reply to {buddy.fname} {buddy.lname[0]} was sent!"})

@app.route("/users/forgotpassword", methods=["POST"])
def send_password():
    """If email exists in system, send verification code."""
    email = request.form.get("email")
    user = crud.get_user_by_email(email)
    #Twilio setup
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    verification = os.environ['TWILIO_VERIFY']
    client = Client(account_sid, auth_token) #client setup for verify API
    email_verification = client.verify.services(verification).verifications.create(to=user.email, channel='email') #send user the email with verification code
    sms_verification = client.verify.services(verification).verifications.create(to=f'+1'+user.phone, channel='sms')

    if user is None:
        flash ("No account found with that email. Please register or try a different email.")
    else:
        flash(f"Verification sent to { user.email } and the phone number you have on file. Please check your email/text and follow login instructions there")
        return render_template("/verification.html", user=user)
    
@app.route("/verify", methods=["POST"])
def verify_user():
    """Login existing users"""
    email = request.form.get("email")
    user_code = request.form.get("code")
    user = crud.get_user_by_email(email)
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    verification = os.environ['TWILIO_VERIFY']
    client = Client(account_sid, auth_token)
    verification_check = client.verify.services(verification).verification_checks.create(to=user.email, code=user_code) 
    sms_verification_check = client.verify.services(verification).verification_checks.create(to=f'+1'+user.phone, code=user_code)
    print(verification_check.status) 
    print(sms_verification_check.status) 
    if verification_check.status or sms_verification_check.status == "approved":
            session["user_id"] = user.user_id
            session["user_email"] = user.email
            session["fname"] = user.fname
            flash(f"Welcome back, {user.email}! You can change your password by updating it below.")
            return redirect("/my_profile")
    else:
        flash("Incorrect code. Please try again")
        return redirect("/verify")
    
@app.route("/edit_profile")
def edit_profile():
    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    return render_template("edit_profile.html", user=user)

@app.route("/update_user", methods=["POST"])
def save_profile():
    #get users variables from form, if variable is not None, then update
    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    email = request.form.get("email")
    if email is not None:
        user.email = email
    password = request.form.get("password")
    if password is not None:
        user.password = password
    fname = request.form.get("fname")
    if fname is not None:
        user.fname = fname
    lname = request.form.get("lname")
    if lname is not None:
        user.lname = lname
    gender = request.form.get("gender")
    if gender is not None:
        user.gender = gender
    pronouns = request.form.get("pronouns")
    if pronouns is not None:
        user.pronouns = pronouns
    about_me = request.form.get("about_me")
    if about_me is not None:
        user.about_me = about_me
    phone = request.form.get("phone")
    if phone is not None:
        user.phone = phone
    db.session.add(user)
    db.session.commit()
    flash("Your changes have been saved!")
    return redirect("/my_profile")

@app.route("/delete")
def delete_messages():
    user_id = session["user_id"]
    crud.delete_messages(user_id)
    return redirect("/messages")
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

