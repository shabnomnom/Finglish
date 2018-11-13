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

    print(req.url)

    # saving the request as a json file 
    # request already return a python dictionary 
    json_dict = req.json()
    print(json_dict)

    item_dict = json_dict["items"]


    words_url = []
    for item in item_dict: 
        if item["country"] == "Iran" and item["langname"] == "Persian":
            words_url.append(item["pathmp3"])
            print(words_url[0])
    return words_url[0]

# word_url("سلام")

# <audio controls="">
#   <source src="https://apifree.forvo.com/audio/243b2j1j2n2d1j3l3i333a3q2c362k3b222f2c2k2f3j351b2q2b2k362k2i2i1f1f1b3n392q22383g3n1h2n371b2p252n293p1j2l263j332h3m22231p1l283b1j_22362d1h3n3c1p34243m1g1o2m2m2d1g2n26341f2c2h1t1t" type="audio/mpeg">
# Your browser does not support the audio element.
# </audio>
        





