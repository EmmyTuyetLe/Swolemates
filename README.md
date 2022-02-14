# Swolemates

Swolemates was inspired by the numerous comments I heard from others, particularly women, regarding how they wish they could go to the gym and workout, but they feel too intimidated to go alone. 

Swolemates helps users overcome a fear of going to the gym alone - or just those looking to find a workout buddy for more fun and support. Users are able to search for gyms by type of gym such as a rockclimbing gym and by location using the Yelp Fusion API. They can view members who also favorited a gym and save interesting profiles and send messages to these users to plan their next workout session!

Users can either create an account or sign in with their Google Account (using OAuth 2.0 protocol). All passwords are hashed and salted with werkzeug or bcrypt.

The application also uses [Faker library](https://faker.readthedocs.io/en/master/) to assist in seeding an initial set of imaginary users.

## Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [Version 2.0](#version2)

## <a name="technologies"></a>Tech Stack
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br/>
APIs: Yelp Fusion, Google Sign-In, Bcrypt, Werkzeug, Twilio Verify, Twilio SMS, Twilio SendGrid<br/>
Libraries: Faker <br/>

## <a name="features"></a>Features
The following is a walkthrough of the User Experience:

### Login, Registration, Permissions

![Homepage](/static/img/homepage.mov "Homepage")

The main homepage displays a link for the user to login or register

Users can register and login using the form, or Google OAuth. If they have forgotten their password, they can get a verification code texted/emailed to them using Twilio Verify and SendGrid API.

![Login](/static/img/login.jpg "Login")

### User Profile

![User Profile](/static/img/profile.png "User Profile")

Users are able to edit their personal information at any time from their profile page by clicking "Update your profile".

### Search Results

![Search Results](/static/img/search.png "Search")

Users can enter in any search term such as "climbing", "kickboxing", or "powerlifting" and by location using city, zipcode etc to find gyms near them. Users are able to save a location as a favorite location


### Gym Users

![Gym Users](/static/img/users.png "Gym users")

Users are able to browse users who favorited a gym location. They can save these users as "swolemates" they are interested in working out with and send them a message. When an user recieves a new message, they will be notified instantly via text from Twilio SMS. 

### Saved Swolemates and Message Inbox
![Swolemates](/static/img/swolemates.png "Swolemates")
Users can see their saved swolemates, along with received message inbox and a sent message inbox. From the swolemates page, users can unsave buddies they are no longer interested in working out with.

![Messages](/static/img/messages.png "Messages")

![Sent Messages](/static/img/sent.png "Sent Messages")


## Installation

To run Swolemates:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/EmmyTuyetLe/swolemates
```

Create and activate a virtual environment inside your Swolemates directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip3 install -r requirements.txt
pip3 install Faker
pip3 install polyline
pip3 install requests
pip3 install Authlib
```

Sign up to use [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3/get_started), [Twilio Verify API ](https://www.twilio.com/docs/verify/api), [Twilio SMS API ](https://www.twilio.com/docs/sms/api), [SendGrid Email API ](https://sendgrid.com/solutions/email-api/)

Obtain OAuth 2.0 credentials from the Google API Console(https://console.developers.google.com/). Authorize the following origins:
```
http://localhost
http://localhost:5000
```

Authorize the following redirect URI:
```
http://localhost:5000/authorize
```

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export YELP_API_KEY="YOUR_KEY_HERE"
export GOOGLE_CLIENT_ID="YOUR_KEY_HERE"
export GOOGLE_CLIENT_SECRET="YOUR_KEY_HERE"
export TWILIO_ACCOUNT_SID="YOUR_KEY_HERE"
export TWILIO_AUTH_TOKEN="YOUR_KEY_HERE"
export SENDGRID_API_KEY="YOUR_KEY_HERE"
export TWILIO_VERIFY="YOUR_KEY_HERE"
export TWILIO_PHONE="YOUR_KEY_HERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up and seed 🌱 the database with sample data:

```
createdb swolemates
python -i model.py
python -i seed.py.py
```

Run the app:

```
python server.py
```

You can now navigate to "localhost:5000/ "to access Swolemates.


## For Version 2.0
Add ability for users to:
* Block and report abusive users
* Hide individual messages in an user's inbox

