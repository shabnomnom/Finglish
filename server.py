
"""Finglish Dictionary """

from jinja2 import StrictUndefined
from sqlalchemy import func

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Word, Vocabulary, connect_to_db, db
import random 

import api_call 

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
# app.jinja_env.undefined = StrictUndefined



@app.route('/')
def index():
    """homepage"""
    # if the user is logged in , show their homepage 
    if session:
        user_id = session['current_user_id']

    return render_template('homepage.html', user_id=user_id)

@app.route('/words')
def all_words():
    """view all users """
    words = Word.query.limit(5)
    pronounciation_dict = {}

    for word in words: 
        if api_call.word_url(word.farsi_word) != None:
            pronounciation_dict[word.farsi_word] = api_call.word_url(word.farsi_word)
        else:
            flash("pronounciation for this word is not available")
    

    return render_template ("/words_list.html", words=words,
    pronounciation_dict=pronounciation_dict )



@app.route('/users')
def all_users():
    """view all users """
    users = User.query.all()

    return render_template("user_list.html", users=users )


# word.word_id is not defined and misleading syntax for python
# change that with the word_id to create a new variable out of the number 
#that route returns 

@app.route('/registration')
def registeration_form():
    """Loading registration page"""
    return render_template("registration.html")

@app.route('/registration', methods=["POST"])
def registeration_process():
    """handeling registration"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    country = request.form.get('country')

    if db.session.query(User).filter(User.email == email).all():
        flash("This email has already been registered to an existing user, please log in.")
        return render_template("log_in.html")
    else:

        new_user = User(first_name=first_name,last_name=last_name,
            email=email, password=password, age=age, country=country)

        db.session.add(new_user)
        db.session.commit()

        app.logger.info(request.form)

        return redirect("/users/{}".format(new_user.user_id))

@app.route('/log_in')
def view_login():
    """render log in page"""
    return render_template("log_in.html")

@app.route('/log_in', methods=["POST"])
def login_process():
    """handeling login process"""

    email_address = request.form.get('email')
    password= request.form.get('password')

    # app.logger.info(email_address)
    # app.logger.info(password)


    #check if the entered password match with the password form the existing 
    #username 
    current_user = db.session.query(User).filter(User.email == email_address).one()
    app.logger.info(current_user)

    if current_user.password == password:
        #putting a session on the user id to be able to log it out, while logged in 

        session['current_user_id'] = current_user.user_id

        app.logger.info(str(session['current_user_id']))

        flash("welcome {} you are logged in".format(current_user.first_name))
        return redirect (f'/users/{current_user.user_id}')


    else: 
        flash ("invalid password, please try again")
        return redirect("/log_in")

@app.route('/log_out', methods=["POST"])
def logout_process():

    if session:
        session.clear()
        flash("you are logged out")
    return redirect("/")

def lesson_generator(user_id):
    words = db.session.query(Word).all()
    lesson_one = random.choices(words,k=10)

    #create an emtpy list outside of the for loop and append the vocabs as you
    # as you commit to the vocabyoulary list 
    vocab_list = [] 

    for word in lesson_one: 
        user_vocab = Vocabulary(user_id=user_id, word_id=word.word_id)
        vocab_list.append(user_vocab)
        db.session.add(user_vocab)
        db.session.commit()


@app.route("/users/<user_id>")
def show_user_homepage(user_id):
    """show the user detail for the specific user id"""

    user = db.session.query(User).filter(User.user_id == user_id).first()
    first_name = user.first_name
    last_name = user.last_name
    country = user.country

    #lesson_generator(user_id)


    words = db.session.query(Word).all()
    lesson_one = random.choices(words,k=10)

    #create an emtpy list outside of the for loop and append the vocabs as you
    # as you commit to the vocabyoulary list 
    vocab_list = [] 

    for word in lesson_one: 
        user_vocab = Vocabulary(user_id=user_id, word_id=word.word_id)
        vocab_list.append(user_vocab)
        db.session.add(user_vocab)
        db.session.commit()
    print("user vocab succesfully added")
    # user_vocab.word.farsi_word

    




    return render_template("user_homepage.html", first_name=first_name,
    last_name = last_name, user= user, country=country, 
    lesson_one=lesson_one, vocab_list=vocab_list)



















































if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000)
