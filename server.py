"""Server for swolemates app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/businesses/search")
def all_locations():
    """Search for businesses by keyword, category, location, price level, etc.."""

    locations = crud.get_location()

    return render_template("locations.html", locations=locations)


@app.route("/businesses/{id}")
def show_location(location_id):
    """Get rich business data, such as name, address, phone number, photos, Yelp rating, price levels and hours of operation."""

    locations = crud.get_location_by_id(location_id)

    return render_template("location_details.html", locations=locations)


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        crud.create_user(email, password)
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/locations/<location_id>/save", methods=["POST"])
def save_location(location_id):
    """Save a location."""

    logged_in_email = session.get("user_email")
    saved_location = request.form.get("location")

    if logged_in_email is None:
        flash("You must log in to save a location.")
    elif not saved_location:
        flash("Error: you didn't select a favorite location.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        location = crud.get_location_by_id(location_id)

    return redirect(f"/locations/{location_id}")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

