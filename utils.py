import os
import requests
import urllib  # Just use requests. You dont need urllib

from bs4 import BeautifulSoup


def scrape():
    # get the resource
    url = 'http://mylanguages.org/farsi_vocabulary.php'

    # open the page and read it
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')

    # get all the tables
    tables = soup.find_all('table')

    print(tables)

    # whatever this does covert my data to a csv
    # tr is row tag
    # th is column tag
    with open('vocabs_#.csv', 'w') as csv:
        for row in tables[1].find_all('tr'):
            line = ""
            for td in row.find_all(['td', 'th']):
                line += td.text + ','
            # csv.write(line + '\n')
    # ran tables[0] and table [1] to have all the tables save the data in


def word_url(farsi_word):
    """Return the url for a word pronunciation."""

    key = os.getenv('forvo_key')
    api_url = "https://apifree.forvo.com/key/"
    url = f"{api_url}/{key}/format/json/action/word-pronunciations/word/{farsi_word}/language/fa"

    # https://apifree.forvo.com/key/95a12f9924eaad8e79c2a57a985fe650/format/xml/action/word-pronunciations/word/cat/language/en

    response = requests.get(url)

    # print(req.url)

    # saving the request as a json file 
    # request already return a python dictionary 
    json_dict = response.json()
    # print("json_dict:",json_dict)
    if json_dict:
        item_dict = json_dict["items"]
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
