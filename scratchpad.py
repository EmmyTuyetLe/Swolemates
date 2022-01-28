# # import requests
# # url = "https://api.yelp.com/v3/businesses/search"
# # headers = {"Authorization": "Bearer mUOoEuwbg4In0FAGUm041a9Std20NoqFWNgw1i36aP8pnVuFYFn5RcKqTcamjM21niuNO9oYfjGexB2zOxGlgGBy8Vd1KfqOXKi6b2SvU2Coy5hzIprEWYW3OgreYXYx" }
# # params = {"term": "gyms", "location": "San Jose"}
# # results = requests.get(url, params=params, headers=headers)

# # results_dict = results.json()
# # businesses = results_dict["businesses"]

# # bus1 = businesses[1]

# {% for location in businesses %}
#     {% if location["categories"] %}
#         {% for index in range(len(categories)) %}   
#             <p>Categories: {{categories[index]["title"]}}</p>
# {% endfor %}
# {% endif %}
# {% endfor %}

# <p><u><b><a href="/fav_location">Click</a></u></b> to save this result as your favorite gym</p>


# #Write a function that takes in a list of strings. Return the longest string in the list.
# longest = "hi"
# words=["cat", "kitten"]
# def wordcount(words):
#     longest = ""
#     for word in words:
#         if len(longest) == 0 or len(word) > len(longest):
#             longest = word
#     return longest

# # Write a function that takes in a string and returns a character count dictionary. For example, 'catty' => {'c': 1, 'a': 1, 't': 2, 'y': 1}
# def char_count(str):
#     count = {}
#     for char in str:
#         count[char] = count.get(char, 0) + 1 # start each char count at 0 then add 1

#     return count




    