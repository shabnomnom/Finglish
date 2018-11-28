
"""Finglish Dictionary """

from jinja2 import StrictUndefined
from sqlalchemy import func, and_

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
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
    #if the user is logged in , show their homepage 
    # session might have other stuff in it so it is safe to just check
    #to see the user id in the session keys 

    if 'current_user_id' in session.keys():
        user_id = session['current_user_id']
        return render_template('homepage.html', user_id=user_id)
    else:

        return render_template('homepage.html')

@app.route('/words')
def all_words():
    """view all words """
    
    return render_template("words_list.html")

@app.route('/words', methods=["POST"])
def search_word():
    """search for a word """

    english = request.form.get("english")
    print("post word",english)

    searched_word = db.session.query(Word).filter(Word.english == english).first() 
    print("query word", searched_word) 

    return render_template("words_list.html", searched_word=searched_word)

@app.route('/pronouciation/<farsi>')
def pronunciation(farsi):
    """getting the pronunciation for each word """

    # Do api_call(farsi_word)
    # Return simple json of {'url': '{farvo_url}'}
    json_payload = { 'url': api_call.word_url(farsi)}
    return jsonify(json_payload)

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

    # Can probably optimize this by querying by ID or email
    if db.session.query(User).filter(User.email == email).all():
        flash("This email has already been registered to an existing user, please log in.")
        return render_template("log_in.html")
    else:

        new_user = User(first_name=first_name,last_name=last_name,
            email=email, password=password, age=age, country=country)

        db.session.add(new_user)
        db.session.commit()
        app.logger.info(request.form)
        app.logger.info("about to generate lessons")
    
        #generate 5 lessons for users when they register 
        lesson_generator(new_user.id)

        return redirect("/users/{}".format(new_user.id))

@app.route('/log_in')
def view_login():
    """render log in page"""
    return render_template("log_in.html")

@app.route('/log_in', methods=["POST"])
def login_process():
    """handeling login process"""

    email_address = request.form.get('email')
    password = request.form.get('password')

    #check if the entered password match with the password form the existing 
    #username 
    current_user = db.session.query(User).filter(User.email == email_address).one()
    app.logger.info(current_user)

    if current_user.password == password:
        #putting a session on the user id to be able to log it out, while logged in 

        session['current_user_id'] = current_user.id

        app.logger.info(str(session['current_user_id']))

        flash("welcome {} you are logged in".format(current_user.first_name))
        return redirect (f'/users/{current_user.id}')

    else: 
        flash ("invalid password, please try again")
        return redirect("/log_in")

@app.route('/log_out', methods=["POST"])
def logout_process():
    """ give the option of logging out if the user is logged in"""
    if 'current_user_id' in session.keys():
        session.clear()
    flash("you are logged out")
    return redirect("/")

def lesson_generator(user_id):
    """generate 10 random words for each lesson """
    
    #take all the words for a user id  and then take those out of the words table 
    # before picking the 10 random word out of the those word 
    for num in range(1,6):
        lesson = db.session.query(Word)\
            .outerjoin(Vocabulary, and_(Word.id == Vocabulary.word_id, Vocabulary.user_id == user_id))\
            .filter(Vocabulary.word_id == None)\
            .order_by(func.random())\
            .limit(10)\
            .all()
        print("words", lesson)

        #create an emtpy list outside of the for loop and append the vocabs as you
        # as you commit to the vocabyoulary list 
        vocab_list = [] 
        for word in lesson: 
            user_vocab = Vocabulary(user_id=user_id, word_id=word.id,
            lesson_num = num)

            vocab_list.append(user_vocab)
            db.session.add(user_vocab)
            db.session.commit()
        print("lesson 1-5 succesfully created ")

def lesson_generator_new(user_id, lesson_num):
    # getting all the words, removing the words that the user already knows and getting 10 random ones
    lesson = db.session.query(Word)\
        .outerjoin(Vocabulary, and_(Word.id == Vocabulary.word_id, Vocabulary.user_id == user_id))\
        .filter(Vocabulary.word_id == None)\
        .order_by(func.random())\
        .limit(10)\
        .all()
    
    print("words", lesson)

    #create an emtpy list outside of the for loop and append the vocabs as you
    # as you commit to the vocabyoulary list 
    vocab_list = [] 
    for word in lesson: 
        user_vocab = Vocabulary(user_id=user_id, word_id=word.id,
        lesson_num = lesson_num)

        vocab_list.append(user_vocab)
        db.session.add(user_vocab)
        db.session.commit()

@app.route("/users/<user_id>")
def show_user_homepage(user_id):
    """show the user detail for the specific user id"""

    user = db.session.query(User).filter(User.id == user_id).first()
    first_name = user.first_name
    last_name = user.last_name
    country = user.country
    user_id = user.id

    return render_template("user_homepage.html", first_name=first_name,
    last_name = last_name, user= user, country=country)


@app.route("/users/<user_id>/<int:lesson_num>")
def show_lesson_vocabs(user_id,lesson_num):
    """show lesson vocabs """
    # user_id = session["current_user_id"]
    # print (user_id)

    lesson_vocabs_query= db.session\
    .query(Vocabulary)\
    .filter(Vocabulary.user_id == user_id,Vocabulary.lesson_num == lesson_num)\
    .all()

    next_page = lesson_num+1 

    #make a dic of answers where word_id are keys 
    #empty the answer dic before making it again per lesson 
    if 'answer_dict' in session:
        session.pop('answer_dict')
    session['answer_dict'] = {}

    return render_template("user_lesson.html",
    lesson_vocabs_query= lesson_vocabs_query,
    lesson_num = lesson_num,
    user_id=user_id,next_page=next_page)
 
@app.route("/users/<user_id>/<lesson_num>/<word_id>", methods=["GET", "POST"])
def validate_answers(user_id,lesson_num,word_id):
    """validating answers and reporting a feedback """

    lesson_vocabs_query= db.session\
    .query(Vocabulary)\
    .filter(Vocabulary.user_id == user_id,Vocabulary.lesson_num == lesson_num)\
    .all()

    word_query = db.session.query(Word)\
    .filter(Word.id==word_id)\
    .first()

    current_word_id = int(word_query.id)
    print(current_word_id)

    next_word = None
    back_word = None
    for i in range(len(lesson_vocabs_query)):

        # print("query item",lesson_vocabs_query[i])
        if i != (len(lesson_vocabs_query) - 1):
            if lesson_vocabs_query[i].word_id == current_word_id:
                next_word = lesson_vocabs_query[i+1].word_id 
            
                answer = request.form.get("answer")

                if answer == "correct":
                    session['answer_dict'][word_id] = 1
                    flash("correct answer is been saved") 
                if answer == "incorrect":
                    session['answer_dict'][word_id] = 0
                    flash("incorrect answer is been saved")

        if i> 0:
            back_word = lesson_vocabs_query[i-1].word_id

        # create an dictunary of answers, where word ids are keys, 
        # and answers are boolian 
    if request.method == "GET": 
            return render_template("flashcard.html",word_query=word_query,
            lesson_vocabs_query=lesson_vocabs_query,user_id=user_id,
            lesson_num=lesson_num,
            word_id=word_id, next_word=next_word, back_word=back_word)        
   
    else:
        return redirect(f"/users/{user_id}/{lesson_num}/{word_id}")

@app.route("/users/<user_id>/<lesson_num>/<word_id>/result", methods=["Post"])
def showlesson_result(user_id,lesson_num, word_id):
    """show result of the flashcard"""
    print("-----------------")

    answer = request.form.get("answer")
    if answer == "correct":
        session['answer_dict'][word_id] = 1
        flash("correct answer is been saved") 
    if answer == "incorrect":
        session['answer_dict'][word_id] = 0
        flash("incorrect answer is been saved")

    result_sum = sum(session['answer_dict'].values())
    result_total = len(session['answer_dict'])
    result = ((result_sum)/result_total)*100
    
    

    return render_template("lesson_result.html", result=result, lesson_num=lesson_num)


























































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
