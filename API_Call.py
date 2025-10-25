# -*- coding: utf-8 -*- 
from sys import argv
from pprint import pprint 
import json 
import requests
import os 

# Check if forvo_key environment variable is set
if 'forvo_key' not in os.environ:
    print("⚠️  Warning: 'forvo_key' environment variable not set. Some features may not work. Set it with: export forvo_key='your_actual_forvo_key'")
    forvo_key = None
else:
    forvo_key = os.environ["forvo_key"]  # os saves the token from the secrets.sh to a dictionary
                                                   # called os.environ.
                                                   # Run the source secrets.sh in the terminal before using.
def word_url(farsi):
    if forvo_key is None:
        print("⚠️  Forvo API key not set. Pronunciation feature unavailable.")
        return None
    
    key = forvo_key
    url = f"https://apifree.forvo.com/key/{key}/format/json/action/word-pronunciations/word/{farsi}/language/fa"
    # Example URL format (with placeholder key): https://apifree.forvo.com/key/YOUR_KEY_HERE/format/xml/action/word-pronunciations/word/cat/language/en

    req = requests.get(url)
    # print(req.url)
    # saving the request as a json file 
    # request already return a python dictionary 
    json_dict = req.json()
    # print("json_dict:",json_dict)
    if json_dict == {}:
        return None
    else:
        item_dict = json_dict["items"]
        # print(item_dict)
        words_url = []
        for item in item_dict:
            print("item:", item["pathmp3"] ) 
            if item["langname"] == "Persian":
                words_url.append(item["pathmp3"])
                # print("first url with conditions met:",words_url[0])
            else: 
                # print("first url with conditions met:","None")
                return None
        return words_url[0]

# word_url(u"کانادا")

# <audio controls="">
#   <source src="https://apifree.forvo.com/audio/243b2j1j2n2d1j3l3i333a3q2c362k3b222f2c2k2f3j351b2q2b2k362k2i2i1f1f1b3n392q22383g3n1h2n371b2p252n293p1j2l263j332h3m22231p1l283b1j_22362d1h3n3c1p34243m1g1o2m2m2d1g2n26341f2c2h1t1t" type="audio/mpeg">
# Your browser does not support the audio element.
# </audio>
        





