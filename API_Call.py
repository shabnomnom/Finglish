from sys import argv
from pprint import pprint 
import json 
import requests
import os 

forvo_key = os.environ["forvo_key"]  # os saves the token from the secrets.sh to a dictionary
                                                   # called os.environ.
                                                   # Run the source secrets.sh in the terminal before using.



key = forvo_key
farsi_word = "سلام"
url="https://apifree.forvo.com/key/" + key + "/format/json/action/word-pronunciations/word/" + farsi_word + "/language/fa"


# https://apifree.forvo.com/key/95a12f9924eaad8e79c2a57a985fe650/format/xml/action/word-pronunciations/word/cat/language/en

req = requests.get(url)

# print(req.url)

# saving the request as a json file 
# request already return a python dictionary 
json_dict = req.json()
# print(json_dict
#     )
item_dict = json_dict["items"]


def word_url(item_dict):
    words_url = []
    for item in item_dict: 
        if item["country"] == "Iran" and item["langname"] == "Persian":
            words_url.append(item["pathmp3"])
        return words_url

word_url

        





