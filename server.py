"""Server for swolemates app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import os
from yelp.client import Client
MY_API_KEY = "Bearer mUOoEuwbg4In0FAGUm041a9Std20NoqFWNgw1i36aP8pnVuFYFn5RcKqTcamjM21niuNO9oYfjGexB2zOxGlgGBy8Vd1KfqOXKi6b2SvU2Coy5hzIprEWYW3OgreYXYx"
client = Client(MY_API_KEY)
import crud


from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/login", methods=["POST"])
def login():
    """Login existing users"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user:
        if user.email == email and user.password == password:
            session["user_email"] = user.email
            flash(f"Welcome back, {user.email}!")
            return redirect("/")
    else:
        flash("Incorrect password or email. Please try again")
    return redirect("/login")

@app.route("/login_button")
def login_page():
    """Tell user if they are logged in or not"""
    if session.get("user_id"):
        flash("You're already logged in")
    else:
        new_session = session.get("user_id")   
        return render_template("login.html", new_session=new_session)
    return redirect("/")

@app.route("/logout")
def logout():
    """Logout users in session"""
    if session.get("user_id"):
        session.clear()
        flash("successfully logged out.")
    else:
        flash("Already logged out")
    return redirect("/")

@app.route("/user")
def to_user_profile():
    """For user to view their profile"""
    if session.get("user_id"):
        return render_template("user.html")
    else:
        flash("Login to see your user page")
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
    user = crud.get_user_by_email(email)
    if user:
        flash("That email is already associated with an account.")
    else:
        crud.create_user(email, password)
        flash("Account created! Please log in.")
    
    return redirect("/login_button")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

