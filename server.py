"""Server for swolemates app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import os
from yelp.client import Client
MY_API_KEY = "Bearer mUOoEuwbg4In0FAGUm041a9Std20NoqFWNgw1i36aP8pnVuFYFn5RcKqTcamjM21niuNO9oYfjGexB2zOxGlgGBy8Vd1KfqOXKi6b2SvU2Coy5hzIprEWYW3OgreYXYx"
import requests
import crud

url = "https://api.yelp.com/v3/businesses/search"
headers = {"Authorization": "Bearer mUOoEuwbg4In0FAGUm041a9Std20NoqFWNgw1i36aP8pnVuFYFn5RcKqTcamjM21niuNO9oYfjGexB2zOxGlgGBy8Vd1KfqOXKi6b2SvU2Coy5hzIprEWYW3OgreYXYx" }
params = {"term": "gyms", "location": "San Jose", "limit": 50, "radius": 50}
results = requests.get(url, params=params, headers=headers)
results_dict = results.json()
businesses = results_dict["businesses"]

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

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

    return render_template("users.html", users=users)


@app.route("/create-user", methods=["POST"])
def create_user():
    """Create new user account"""
    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    user = crud.get_user_by_email(email)
    if user:
        flash("That email is already associated with an account.")
    else:
        crud.create_user(email, password, fname, lname)
        flash("Account created! Please log in.")
    
    return redirect("/login")

@app.route("/search")
def search(search_term="gyms", location="San Jose", search_limit=10):
    search_term = request.args.get("term")
    print(search_term)
    location = request.args.get("location")
    print(location)
    params = {"term": search_term, "location": location, "limit": search_limit}
    results = requests.get(url, params=params, headers=headers)
    results_dict = results.json()
    businesses = results_dict["businesses"]
    print(businesses)
    return render_template("location_results.html", businesses=businesses)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

