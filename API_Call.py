from sys import argv
from pprint import pprint 
import json 
import requests
import os 

forvo_key = os.environ["forvo_key"]  # os saves the token from the secrets.sh to a dictionary
                                                   # called os.environ.
                                                   # Run the source secrets.sh in the terminal before using.




def word_url(farsi_word):

    key = forvo_key
    url="https://apifree.forvo.com/key/" + key + "/format/json/action/word-pronunciations/word/" + farsi_word + "/language/fa"

    # https://apifree.forvo.com/key/95a12f9924eaad8e79c2a57a985fe650/format/xml/action/word-pronunciations/word/cat/language/en

    req = requests.get(url)

    #print(req.url)

    # saving the request as a json file 
    # request already return a python dictionary 
    json_dict = req.json()
    #print(json_dict)

    item_dict = json_dict["items"]


    words_url = []
    for item in item_dict: 
        if item["country"] == "Iran" and item["langname"] == "Persian":
            words_url.append(item["pathmp3"])
            print(words_url[0])
        return words_url[0]

# word_url("سلام")

        





