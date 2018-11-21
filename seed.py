""" Using this to seed the finglish_app form seed_data"""


from sqlalchemy import func
from model import User 
from model import Word 
from model import Vocabulary  



from model import connect_to_db, connect_to_db, db 
from server import app 

# this is the test data to test the seeding process
# otherwise the real data will be populated from the user input form 
# def load_users():
#     """load users from u.user into database""" 

#     ## print user class
#     print("Users")

#     #delete before adding new user so you don't doplicate users data
#     User.query.delete()

#     # Read u.user file and insert data
#     with open("seed.data/u.user") as file:
#         for row in file:
#             row = row.rstrip()
#             _,age, gender, occupation, zipcode = row.split("|")

#             user = User(
#                         age=age,
#                         zipcode=zipcode)

#             # We need to add to the session or it won't ever be stored
#             db.session.add(user)

    # Once we're done, we should commit our work
    # db.session.commit()

def load_words():
    """load words data"""

    ## printing the table? 
    print("Words")


    Word.query.delete()

    with open("seed.data/vocabs.csv") as file:
        for row in file:
            row= row.rstrip()

            english, farsi_phonetic,farsi,_ = row.split(",")

            word = Word(english= english.lower(),
            farsi_phonetic=farsi_phonetic,farsi =farsi)
            db.session.add(word)

    db.session.commit()



###########################
if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    load_words()
    # load_vocab_list()







