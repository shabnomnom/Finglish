"""Models and database functions for finglish project."""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

####################################################################################

# Model functions

class User(db.Model):
    """User of finglish website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} email={}>".format(self.user_id, self.email)


class Word(db.Model):
    """word info """

    __tablename__ = "words"

    word_id = db.Column(db.Integer, autoincrement= True, primary_key =True)
    english_word = db.Column(db.String(100), nullable=False)
    farsi_phenetic= db.Column(db.String(100), nullable=False)
    farsi_word = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(500), nullable=True)
    ## picture to be determined 

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Word english_word={} farsi_word={}>".format(self.english_word,
         self.farsi_word)



class Vocabulary(db.Model):
    """user vocabs """

    __tablename__= "vocabs"

    vocab_id = db.Column(db.Integer, autoincrement= True, primary_key =True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    word_id = db.Column(db.Integer,db.ForeignKey('words.word_id'))

    user = db.relationship('User', backref=db.backref('vocabs'), order_by=vocab_id)

    word = db.relationship('Word', backref=db.backref('vocabs'), order_by=vocab_id)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Vocabs  vocab_id={} user_id={} word_id={}>".format(self.vocab_id,
        self.user_id , self.word_id)



   



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///finglish'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")