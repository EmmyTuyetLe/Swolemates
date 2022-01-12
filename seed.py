"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server
import requests

os.system("dropdb swolemates")
os.system("createdb swolemates")

model.connect_to_db(server.app)
model.db.create_all()

# Create locations
url = "https://api.yelp.com/v3/businesses/search"
headers = {"Authorization": "Bearer mUOoEuwbg4In0FAGUm041a9Std20NoqFWNgw1i36aP8pnVuFYFn5RcKqTcamjM21niuNO9oYfjGexB2zOxGlgGBy8Vd1KfqOXKi6b2SvU2Coy5hzIprEWYW3OgreYXYx" }
params = {"term": "gyms", "location": "San Jose"}
results = requests.get(url, params=params, headers=headers)

results_dict = results.json()
businesses = results_dict["businesses"]

# location1= create_location(businesses1["id"], businesses1["name"])
for n in range(10):
    location = crud.create_location(businesses[n]["id"], businesses[n]["name"])
    

# Create 20 users; 
users_db = []
for n in range(20):
    email = f"user{n}@test.com"  
    password = "test"

    user = crud.create_user(email, password)
    
#have some users save other users
#should I randomly generate an user id and buddy id from the existing users db?
    # for _ in range(20):
    #     buddy_id = randint(1, 20)
    #     user_id = randint(1, 20)
    #     if buddy_id != user_id:
    #         crud.create_buddy(buddy_id, user_id)

