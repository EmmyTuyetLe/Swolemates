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
params = {"term": "gyms", "location": "San Jose"}
results = requests.get(url, params=params, headers=headers)
results_dict = results.json()
businesses = results_dict["businesses"]

# location1= create_location(businesses1["id"], businesses1["name"])
for n in range(10):
    location = crud.create_location(businesses[n]["id"], businesses[n]["name"])
    


# Create 20 users;
users_db = []
# gender_options = ["Cisgender-female", "Non-binary/non-conforming", "Transgender-female", "Transgender-male", "Cisgender-male"] 
for n in range(20):
    fname = fake.first_name()
    lname = fake.last_name()
    # gender = choice(gender_options)
    domain = fake.free_email_domain()
    email = f'{fname}.{lname}@{domain}' 
    password = "test"

    user = crud.create_user(fname=fname, lname=lname, email=email, password=password)
    users_db.append(user)
    
# # have some users save other users
# # user1 = users[0]
# # user2 = users[1]
# # user1.buddies.append(user2)
# # save1 = Save(buddy = user1, user = user2)
# # db.session.add(save1)
# # db.session.commit()

# for user in users_db: 
#     buddy = choice(users_db)
#     user = choice(users_db)

#     if user != buddy:

#         save = crud.create_buddy(buddy, user)

#     else:
#         continue

    

    
    
    

