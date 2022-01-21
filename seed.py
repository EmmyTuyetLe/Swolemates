"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
from faker import Faker

import crud
import model
import server
import requests
fake = Faker()

os.system("dropdb swolemates")
os.system("createdb swolemates")

model.connect_to_db(server.app)
model.db.create_all()

# Create locations
url = "https://api.yelp.com/v3/businesses/search"
headers = {"Authorization": "Bearer mUOoEuwbg4In0FAGUm041a9Std20NoqFWNgw1i36aP8pnVuFYFn5RcKqTcamjM21niuNO9oYfjGexB2zOxGlgGBy8Vd1KfqOXKi6b2SvU2Coy5hzIprEWYW3OgreYXYx" }
params = {"term": "gyms", "location": "Sunnyvale"}
results = requests.get(url, params=params, headers=headers)
results_dict = results.json()
businesses = results_dict["businesses"]

# location1= create_location(businesses1["id"], businesses1["name"])
locations_db = []
for n in range(10):
    location = crud.create_location(businesses[n]["id"], businesses[n]["name"])
    locations_db.append(location.location_id)
    


# Create 40 users;
users_db = []
# gender_options = ["Cisgender-female", "Non-binary/non-conforming", "Transgender-female", "Transgender-male", "Cisgender-male"] 
for n in range(30):
    fname = fake.first_name()
    lname = fake.last_name()
    # gender = choice(gender_options)
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}' 
    password = "test"
    fav_location = choice(locations_db)
    user = crud.create_user(fname=fname, lname=lname, email=email, password=password, fav_location=fav_location)
    users_db.append(user)
    
    
#create saves table  
for n in range(60):
    buddy = crud.get_user_by_id(randint(1,30))
    user = crud.get_user_by_id(randint(1,30))
    if buddy != user:
        crud.create_buddy(buddy=buddy, user=user)

    

    
    
    

