# Finglish 

Finglish is a learning language app that helps users learn new Farsi words using a flashcard system. Inspired by the lack of pronunciation feature in google translate for Farsi language, Finglish brings you pronunciation, translation and phonetic of most common Farsi words using flashcards. Once you are ready, you can take a quiz on each lesson and get an instant result. 

## Table of Contents 
[Tech Stack](#techStack)<br/>
[Requirements](#requirements)<br/>
[Installation](#installation)<br/>
[Features](#features)<br/>
[Future Features](#future_features)

<a name="techStack"/></a>
## Tech Stack 
**Backend:** Python, Flask, SQLAlchemy, PostgreSQL, AJAX<br/>
**Frontend:**  Javascript, Jinja, jQuery, Bootstrap, Html, Css</br>
**Libraries:** Beautiful Soup, </br>
**APIs:** https://api.forvo.com/ </br>

I built a Postgres database of scraped Farsi words and their translations using beautiful soup library. As an auditory learner, I integrated the pronunciation feature for the Farsi words using an API called forvo.com which crowdsources correct pronunciation. I queried my database using SQL alchemy to create on-demand user lessons that come with a set of flashcards. I used JQuery to demonstrate the flashcards content, and finally, integrated a combination of javascript and CSS to create and animate the flashcards and provide quiz results. 


<a name="requirement"/></a>
## Requirements

* Flask==1.0.2
* Flask-DebugToolbar==0.10.1
* Flask-SQLAlchemy==2.3.2
* Jinja2==2.10
* MarkupSafe==1.0
* psycopg2==2.7.5
* SQLAlchemy==1.2.8
* beautifulsoup4
* RequestsSetup

<a name="installation"/></a>
## Installation
1. Pay for forvo.com basic plan and get a secret KEY and save your Forvo Secret key in secret.sh file 

2. Create a virtual environment
        - `$ virtualenv env`
3. Activate virtual environment:
        - `$ source env/bin/activate`
4.Install requirements:
        - ` $ pip install -r requirements.txt`
5. Create database:
        - `$ createdb Finglish`               
6. Create your database tables:
        - ` python3 model.py`
8. Seed your data 
        - `$ seed.py`
9. Source secrets.sh:
        - `$ source secrets.sh`
10. Run the app:
        -`$ python3 server.py`
11. view your app at :
        - http://localhost:5000/
        
<a name="features"/></a>
## Features  
        -register as a new user and log in: 
        ![](lesson.gif)
        


        -Search for a word in search bar 
        -create a new lesson 
   
        - look at your lesson overview 
   
        - look at your flashcard 
   
        - take a quiz 
   
   


