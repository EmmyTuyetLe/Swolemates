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
location_names = []
for n in range(10):
    location = crud.create_location(businesses[n]["id"], businesses[n]["name"], businesses[n]["url"] )
    locations_db.append(location.location_id)
    location_names.append(location.name)
    
# Create 30 female users;
bio = ["In addition to lifting, I love rockclimbing and am looking for someone to get into climbing with! I prefer climbing in the evenings after 5 pm. Open to any gyms within a reasonable distance of Sunnyvale.",
       "Looking to meet someone to lift heavy weights with! Current prs - D: 445, S: 340 B: 275. I prefer to lift in the mornings from 5am to 8am.",
       "New to fitness and feeling anxious about going to the gym, would love someone to start my fitness journey with. Schedule is pretty open! Open to any gyms within a reasonable distance of Sunnyvale.",
       "I love cardio and am looking for someone to do spin/group fitness classes with! Open to mornings or evenings.",
       "I am new to lifting and am hoping to pair up with a more experienced swolemate to help me learn proper form and best practices!",
       "New to lifting and am open to swolemates, but would prefer someone of the same gender please. Open to any gyms within a half hour drive of San Jose."]
users_db = [] 
female = ["Transgender-female", "Transgender-female", "Cisgender-female", "Cisgender-female", "Cisgender-female"]
female_pronouns = ["She/her", "She/her", "She/her"] 
for n in range(30):
    fname = fake.first_name_female()
    lname = fake.last_name()
    gender = choice(female)
    pronouns = choice(female_pronouns)
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}' 
    password = "test"
    about_me = choice(bio)
    fav_location = choice(locations_db)
    phone = fake.phone_number()
    user = crud.create_user(fname=fname, lname=lname, email=email, password=password, 
                        fav_location=fav_location, pronouns=pronouns, gender=gender, about_me=about_me, phone=phone)
    users_db.append(user)
    
# Create 20 nonbinary users;
    
for n in range(20):
    fname = fake.first_name()
    lname = fake.last_name()
    gender = "Non-binary/non-conforming"
    pronouns = "They/them"
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}' 
    password = "test"
    about_me = choice(bio)
    fav_location = choice(locations_db)
    phone = fake.phone_number()

    user = crud.create_user(fname=fname, lname=lname, email=email, password=password, 
                        fav_location=fav_location, pronouns=pronouns, gender=gender, about_me=about_me, phone=phone)
    users_db.append(user)

# Create 20 male users;
    
male = ["Transgender-male", "Transgender-male", "Cisgender-male", "Cisgender-male", "Cisgender-male"]
male_pronouns = ["He/him", "He/him", "He/him"] 
for n in range(20):
    fname = fake.first_name_male()
    lname = fake.last_name()
    gender = choice(male)
    pronouns = choice(male_pronouns)
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}' 
    password = "test"
    about_me = choice(bio)
    fav_location = choice(locations_db)
    phone = fake.phone_number()
    user = crud.create_user(fname=fname, lname=lname, email=email, password=password, 
                            fav_location=fav_location, pronouns=pronouns, gender=gender, about_me=about_me, phone=phone)
    users_db.append(user)
    
#create saves table  
for n in range(50):
    buddy = crud.get_user_by_id(randint(1,30))
    user = crud.get_user_by_id(randint(1,30))
    if buddy != user:
        crud.create_buddy(buddy=buddy, user=user)
        # crud.create_message(buddy=buddy, user=user, message="Hi, nice to meet you. Would love to workout sometime!")


#make specific user for testing
user1 = crud.create_user(fname="Test", lname="Person", email="test@test.com", password="test", pronouns="They/them", gender="Non-binary/non-conforming", about_me="I am a test user.")
user2 = crud.create_user(fname="Swolemates", lname="Admin", email="swolemates.team1@gmail.com", password="test", pronouns="She/her", gender="Non-binary/non-conforming", about_me="I am the Swolemates admin.")
 
#create messages      
crud.create_message(buddy=user1, user=user2, message="Hello, let's be friends!")
crud.create_message(buddy=user1, user=user2, message="Hello, would love to workout sometime. I also go to that gym!")
  
    

    
    
    

