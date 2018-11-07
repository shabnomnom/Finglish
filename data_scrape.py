

#import libraries
import requests 
from bs4 import BeautifulSoup 
import urllib, urllib.parse, urllib.error

#get the resource 
url='http://mylanguages.org/farsi_vocabulary.php'

#open the page and read it 
page = urllib.request.urlopen(url).read()
soup = BeautifulSoup(page, 'html.parser') 

#get all the tables
tables = soup.find_all('table')

print(tables)

# whatever this does covert my data to a csv 
#tr is row tag
# th is column tag 
with open ('vocabs_#.csv', 'w') as csv:
    for row in tables[1].find_all('tr'):
        line = ""
        for td in row.find_all(['td','th']):
            line += td.text + ','
        #csv.write(line + '\n')
        


# ran tables[0] and table [1] to have all the tables save the data in 