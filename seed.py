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
    


# Create 25 male users;
bio = ["In addition to lifting, I love rockclimbing and am looking for someone to get into climbing with! I prefer climbing in the evenings after 5 pm.",
       "Looking to meet someone to lift heavy weights with! Current prs - D: 445, S: 340 B: 275. I prefer to lift in the mornings from 5am to 8am.",
       "New to fitness and feeling anxious about going to the gym, would love someone to start my fitness journey with. Schedule is pretty open!",
       "I love cardio and am looking for someone to do spin/group fitness classes with! Open to mornings or evenings.",
       "I am new to lifting and am hoping to pair up with a more experienced swolemate to help me learn proper form and best practices!",
       "New to lifting and am open to swolemates, but would prefer someone of the same gender please."]
users_db = []
male = ["Non-binary/non-conforming", "Transgender-male", "Transgender-male", "Cisgender-male", "Cisgender-male", "Cisgender-male"]
male_pronouns = ["He/him", "He/him", "He/him", "They/them" ] 
for n in range(25):
    fname = fake.first_name_male()
    lname = fake.last_name()
    gender = choice(male)
    pronouns = choice(male_pronouns)
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}' 
    password = "test"
    about_me = choice(bio)
    fav_location = choice(locations_db)
    user = crud.create_user(fname=fname, lname=lname, email=email, password=password, 
                            fav_location=fav_location, pronouns=pronouns, gender=gender, about_me=about_me)
    users_db.append(user)
    
# Create 30 female users;
    
female = ["Non-binary/non-conforming", "Transgender-female", "Transgender-female", "Cisgender-female", "Cisgender-female", "Cisgender-female"]
female_pronouns = ["She/her", "She/her", "She/her", "They/them" ] 
for n in range(25):
    fname = fake.first_name_male()
    lname = fake.last_name()
    gender = choice(female)
    pronouns = choice(female_pronouns)
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}' 
    password = "test"
    about_me = choice(bio)
    fav_location = choice(locations_db)
    user = crud.create_user(fname=fname, lname=lname, email=email, password=password, 
                        fav_location=fav_location, pronouns=pronouns, gender=gender, about_me=about_me)
    users_db.append(user) 


     
#create saves table  
for n in range(100):
    buddy = crud.get_user_by_id(randint(1,30))
    user = crud.get_user_by_id(randint(1,30))
    if buddy != user:
        crud.create_buddy(buddy=buddy, user=user)
        crud.create_message(buddy=buddy, user=user, message="Hi, nice to meet you. Would love to workout sometime!")
        



    

    
    
    

