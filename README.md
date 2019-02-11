# Finglish 


Finglish is a learning language app that helps users learn new Farsi words using a flashcard system. Inspired by the lack of pronunciation features in google translate for Farsi language, Finglish brings you pronunciation, translation and phonetic of most common Farsi words. In addition to the word search functionality, users are provided with digital flashcards that aid in memorization, as well as quizzes to help validate the words users have learned.

I built a Postgres database of scraped Farsi words and their translations using beautiful soup library. As an auditory learner, I integrated the pronunciation feature for the Farsi words using an API called forvo.com which crowdsources correct pronunciation. I queried my database using SQL alchemy to create on-demand user lessons that come with a set of flashcards. I used Jquery to demonstrate the flashcards content, and finally, integrated a combination of javascript and CSS to create and animate the flashcards and provide quiz results. 


Requirments:

        blinker==1.4
        click==6.7
        Flask==1.0.2
        Flask-DebugToolbar==0.10.1
        Flask-SQLAlchemy==2.3.2
        itsdangerous==0.24
        Jinja2==2.10
        MarkupSafe==1.0
        psycopg2==2.7.5
        SQLAlchemy==1.2.8
        Werkzeug==0.14.1
        beautifulsoup4
        RequestsSetup

Launch and activate a virtual environment

        $ virtualenv env
        $ source env/bin/activate

    Install Python 3.6

    pip install requirements
        
        $ pip install -r requirements.txt


    Create and seed the database

        $ createdb finglish
        $ python model.py
        $ python seed.py

    Launch server

        $ python server.py

    View app at:
    
        http://localhost:5000/
        
   Test it out: 
   -register as new user 
   -search for a word in search bar 
   - log in 
   -create a new lesson 
   - look at your lesson overview 
   - look at your flashcard 
   - take a flashcard quiz 
   
   


