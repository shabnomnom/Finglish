
"""Finglish Dictionary """

from jinja2 import StrictUndefined
from sqlalchemy import func, and_, update

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Word, Vocabulary, connect_to_db, db
import random 

import API_Call

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

@app.route('/dictionary')
def all_words():
    """view all words """
    
    return render_template("words_list.html")

@app.route('/dictionary', methods=["POST"])
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
    json_payload = { 'url': API_call.word_url(farsi)}
    print(jsonify(json_payload))
    return jsonify(json_payload)

@app.route('/users')
def all_users():
    """view all users """
    if session: 
        users = User.query.all()
        return render_template("user_list.html", users=users )
    else: 
        return redirect('/')
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
        session['current_user_id'] = new_user.id 

        #generate 1 lesson for users when they register 
        lesson_generator(new_user.id,1)

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
        # flashing_welcome =flash("welcome {} you are logged in".format(current_user.first_name))
        return redirect (f'/users/{current_user.id}')
    else: 
        # flashing_invalid_password=flash ("invalid password, please try again")
        return redirect("/")

@app.route('/log_out', methods=["POST"])
def logout_process():
    """ give the option of logging out if the user is logged in"""
    if 'current_user_id' in session.keys():
        session.clear()
    # flash("see you next time")
    return redirect("/")

@app.route('/profile/<user_id>')
def user_info(user_id):
    """show user info"""
    user = db.session.query(User).filter(User.id == user_id).first()
    first_name = user.first_name
    last_name = user.last_name
    country = user.country
    age = user.age 
    return render_template("user_info.html", country=country, first_name= first_name,
    last_name=last_name, age=age, user_id=user_id )

def lesson_generator(user_id, lesson_num):
    # getting all the words, removing the words that the user already knows and getting 10 random ones
    
        lesson = db.session.query(Word)\
            .outerjoin(Vocabulary, and_(Word.id == Vocabulary.word_id, Vocabulary.user_id == user_id))\
            .filter(Vocabulary.word_id == None)\
            .order_by(func.random())\
            .limit(11)\
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

@app.route("/users/<user_id>", methods=["GET","Post"])
def show_user_homepage(user_id):
    """show the list of the lessons"""

    english = request.form.get("english")
    print("post word",english)

    searched_word = db.session.query(Word).filter(Word.english == english).first() 
    print("query word", searched_word) 

    user_id = session['current_user_id']
    user = User.query.get(user_id)

    user_lesson_num_tuple = db.session\
    .query(func.max(Vocabulary.lesson_num))\
    .filter(Vocabulary.user_id == user_id)\
    .first()

    user_lesson_num = user_lesson_num_tuple[0]
    print("user lesson num", user_lesson_num)

    if request.method == "GET":  

        return render_template("user_homepage.html", user= user,
        user_lesson_num = user_lesson_num )
    else:
        return render_template("words_list.html",
        searched_word=searched_word)

@app.route("/users/<user_id>/lesson/<int:lesson_num>")
def show_lesson_page(user_id,lesson_num):
    """show lesson vocabs """
    user_id = session["current_user_id"]
    # print (user_id)

    lesson_vocabs_query= db.session\
    .query(Vocabulary)\
    .filter(Vocabulary.user_id == user_id,Vocabulary.lesson_num == lesson_num)\
    .order_by(Vocabulary.vocab_id)\
    .all()

    first_word = lesson_vocabs_query[0].word_id
    session['answer_dict'] = {}

    return render_template("user_lesson.html",
    lesson_num = lesson_num,
    user_id=user_id, word_id=first_word)

@app.route("/users/<user_id>/lesson/<int:lesson_num>/overview")
def show_lesson_vocabs(user_id,lesson_num):
    """show lesson vocabs """

    # user_id = session["current_user_id"]
    # print (user_id)

    lesson_vocabs_query= db.session\
    .query(Vocabulary)\
    .filter(Vocabulary.user_id == user_id,Vocabulary.lesson_num == lesson_num)\
    .order_by(Vocabulary.vocab_id)\
    .all()

    first_word = lesson_vocabs_query[0].word_id
    next_page = lesson_num+1
    

    return render_template("lesson_overview.html",
    lesson_vocabs_query= lesson_vocabs_query,
    lesson_num = lesson_num,
    user_id=user_id,next_page=next_page, word_id=first_word)


@app.route("/users/<user_id>/lesson/<lesson_num>/flashcards/<word_id>", methods=["GET"])
def flashcards(user_id,lesson_num,word_id):
    """show the words in a lesson """

    lesson_vocabs_query= db.session\
    .query(Vocabulary)\
    .filter(Vocabulary.user_id == user_id,Vocabulary.lesson_num == lesson_num)\
    .order_by(Vocabulary.vocab_id)\
    .all()

    word_query = db.session.query(Word)\
    .filter(Word.id==word_id)\
    .first()
    current_word_id = word_query.id
    print (current_word_id)

    # first_vocab = lesson_vocabs_query[0]
    # first_vocab_word_id = first_vocab.word.id 
    next_word = None
    back_word = None
    for i in range(len(lesson_vocabs_query)):

        # print("query item",lesson_vocabs_query[i])
        if i != (len(lesson_vocabs_query) - 1):
            if lesson_vocabs_query[i].word_id ==current_word_id:
                next_word = lesson_vocabs_query[i+1].word_id 

        if i> 0:
            back_word = lesson_vocabs_query[i-1].word_id
            # print("-----------")
            # print(back_word)

    return render_template("flashcards.html",user_id=user_id,
    lesson_num=lesson_num,word_id=word_id,
     next_word=next_word, back_word=back_word, word_query=word_query)        
 
@app.route("/users/<user_id>/lesson/<lesson_num>/quiz/<word_id>", methods=["GET", "POST"])
def validate_answers(user_id,lesson_num,word_id):
    """validating answers and reporting a feedback """
    if 'answer_dict' not in session:
        session['answer_dict'] = {}

    lesson_vocabs_query= db.session\
    .query(Vocabulary)\
    .filter(Vocabulary.user_id == user_id,Vocabulary.lesson_num == lesson_num)\
    .order_by(Vocabulary.vocab_id)\
    .all()

    word_query = db.session.query(Word)\
    .filter(Word.id==word_id)\
    .first()
    current_word_id = word_query.id
    first_word = lesson_vocabs_query[0]
    # print("-------")
    # print("firstwordid",first_word.word_id)
    # print("firstwordfarsai",first_word.word.farsi
    next_word = None
    back_word = None
    for i in range(len(lesson_vocabs_query)):

        # print("query item",lesson_vocabs_query[i])
        if i != (len(lesson_vocabs_query) - 1):
            if lesson_vocabs_query[i].word_id == current_word_id:
                next_word = lesson_vocabs_query[i+1].word_id 
            
                answer = request.form.get("answer")
                previous_word_id = request.form.get("previous_word_id")
                print("____")
                print("answer",answer)
                print("word_id",word_id)
                print("previous word id",previous_word_id)
                print("i",i)

                if answer == "correct" and previous_word_id:
                    session['answer_dict'][previous_word_id] = 1
                    print("dict correct")
                    flash(f"correct answer is been saved {previous_word_id}") 
                if answer == "incorrect" and previous_word_id:
                    session['answer_dict'][previous_word_id] = 0
                    print("dict incorrect")
                    flash("incorrect answer is been saved",current_word_id)

                if i > 0:
                    back_word =lesson_vocabs_query[i-1].word_id
                    # print("-----------")
                    # print(back_word)

    return render_template("flashcard_quiz.html", user_id=user_id,
    lesson_vocabs_query=lesson_vocabs_query,lesson_num=lesson_num, word_query=word_query,
    word_id=word_id, next_word=next_word, back_word=back_word, first_word=first_word)        

    if request.method == "POST":
        return redirect(f"/users/{user_id}/lesson/{lesson_num}/quiz/{word_id}")

@app.route("/users/<user_id>/lesson/<lesson_num>/quiz/<word_id>/result", methods=["Post"])
def showlesson_result(user_id,lesson_num, word_id):
    """show result of the flashcard"""
    print("-----------------")

    answer = request.form.get("answer")
    previous_word_id = request.form.get("previous_word_id")

    if answer == "correct" and previous_word_id:
        session['answer_dict'][previous_word_id] = 1
        # flash("correct answer is been saved") 
    if answer == "incorrect" and previous_word_id:
        session['answer_dict'][previous_word_id] = 0
        # flash("incorrect answer is been saved")

    result_sum = sum(session['answer_dict'].values())
    result_total = len(session['answer_dict'])

    #calculating the first vocab so fr try again ,to go back to beggining 
    #of the lesson
    first_word= db.session\
    .query(Vocabulary)\
    .filter(Vocabulary.user_id == user_id,Vocabulary.lesson_num == lesson_num)\
    .order_by(Vocabulary.vocab_id)\
    .first()

    # make a dic of answers where word_id are keys 
    # empty the answer dic before making it again per lesson 
    if 'answer_dict' in session:
        for word_id in session['answer_dict']:
            if session['answer_dict'][word_id]== 1:
                correct_vocab = db.session\
                .query(Vocabulary)\
                .filter(and_(Vocabulary.user_id == user_id, Vocabulary.word_id == word_id))\
                .first()
                correct_vocab.correct_count += 1
        db.session.commit()
        session.pop('answer_dict')

    return render_template("lesson_result.html",
    lesson_num=lesson_num, user_id=user_id,result_sum=result_sum,
    result_total=result_total, word_id=word_id,
    first_word=first_word)

# TODO: make this a POST ONLY
#add click handeler  to the 
@app.route("/update_seen_count/<word_id>", methods=["POST", "GET"])
def update_seen_count(word_id):
    """update seen count per word"""
    user_id = session['current_user_id']
    print('here: user_id={}, word_id={}'.format(user_id, word_id))
    
    seen_vocab = db.session\
    .query(Vocabulary)\
    .filter(and_(Vocabulary.user_id == user_id, Vocabulary.word_id == word_id))\
    .first()

    print("____________")
    print(seen_vocab.seen_count)
    seen_vocab.seen_count += 1
    # how do i update this?
    db.session.commit()
    return ""

@app.route("/request_new_lesson/<user_id>", methods=["POST", "GET"])
def request_new_lesson(user_id):
    user_id = session['current_user_id']
    user = User.query.get(user_id)
    print("user",user)

    #find the max lesson number and add one to it to generate a lesson 
    # return a tuple 
    user_lesson_num_tuple = db.session\
    .query(func.max(Vocabulary.lesson_num))\
    .filter(Vocabulary.user_id == user_id)\
    .first()

    # print("typeeeeeee",type(user_lesson_num[0]))
    user_lesson_num = user_lesson_num_tuple[0]
    new_lesson_num = user_lesson_num +1 
    lesson_generator(user_id,new_lesson_num)    
    
    return redirect(f"/profile/{user_id}")


# @app.route ("weighted_word/lessons", methods=["POST", "GET"]) 
# def lesson_generator_ww(user_id, lesson_num):





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True 
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000)
