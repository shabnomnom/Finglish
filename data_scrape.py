

#import libraries
import requests 
from bs4 import BeautifulSoup 
import urllib, urllib.parse, urllib.error


url='http://mylanguages.org/farsi_vocabulary.php'

page = urllib.request.urlopen(url).read()
soup = BeautifulSoup(page, 'html.parser') 

tables = soup.find_all('table')

#print(tables)
# whatever this does covert my data to a csv 
with open ('vocabs.csv', 'w') as csv:
    for row in tables[0].find_all('tr'):
        line = ""
        for td in row.find_all(['td','th']):
            if "-" in td:
                td.replace('-',",")
                line += '"' + td.text + '",'
                csv.write(line + '\n')
        

# with open("vocabs.csv") as file:
#     for row in file:
#         if '-' in row:
#             row.replace('-',",")
#             print (row)



