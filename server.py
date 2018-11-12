
"""Finglish Dictionary """

from jinja2 import StrictUndefined

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

    return render_template('homepage.html')

@app.route('/words')
def all_words():
    """view all users """
    words = Word.query.all()

    return render_template("words_list.html", words = words )

# word.word_id is not defined and misleading syntax for python
# change that with the word_id to create a new variable out of the number 
#that route returns 
@app.route('/pronounciation/<id>')
def processing_pronounciation(id):
    """get the pronounciation mp3 from api_call function"""
    app.logger.info(word_id)

    #find farsi_word for word_id is in the database 
    pronounciation_query = db.session.query(Word.farsi_word).filter(Word.word_id == id).one()

    if pronounciation != None:
        word_url(pronounciation_query)
    else:
        flash("pronounciation for this word is not available ")


        return redirect ("/")


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

    return redirect("/<user_id>")

@app.route('/log_in')
def view_login():
    """render log in page"""
    return render_template("log_in.html")

@app.route('/Log_in', methods=["POST"])
def login_process():
    """handeling login process"""

    email_address = request.form.get('email')
    password= request.form.get('password')

    #check if the entered password match with the password form the existing 
    #username 
    current_user = db.session.query(User).filter(User.email == email_address).one()

    if current_user.password == password:
        #putting a session on the user id to be able to log it out, while logged in 

        session['current_user_id'] = current_user.user_id
        flash("welcome {} you are logged in".format(user.first_name))
        return redirect (f'log_in/{user.user_id}')


    else: 
        flash ("invalid password, please try again")
        return redirect("/log_in")

app.route("/log_out", methods=["POST"])
def logout_process():
    if session:
        session.clear()
        flash("you are logged out")
    return redirect("/")


app.route("/<user_id>")
def show_user_homepage(user_id):
    """show the user detail for the specific user id"""

    user = db.session.query(User).filter(User.user_id == user_id).first()
    first_name = user.first_name
    last_name = user.last_name
    age = user.age 
    country = user.country

    words = Word.query.all()
    lesson_one = random.choice(words)


    return render_template("user_homepage.html", first_name=first_name,
    last_name = last_name, age= age, user= user, country=country, 
    lesson_one=lesson_one)




















































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
