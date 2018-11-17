"""Models and database functions for finglish project."""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

####################################################################################

# Model functions
vocab_words = db.Table('vocab_words',
    db.Column('vocab_id', db.Integer, db.ForeignKey('vocabs.id')),
    db.Column('word_id', db.Integer, db.ForeignKey('words.id'))
)

class User(db.Model):
    """User of finglish website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    country = db.Column(db.String(15))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} email={}>".format(self.user_id, self.email)


class Word(db.Model):
    """word info """

    __tablename__ = "words"

    id = db.Column(db.Integer, autoincrement= True, primary_key =True)
    english = db.Column(db.String(100), nullable=False)
    farsi_phonetic= db.Column(db.String(100), nullable=False)
    farsi = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(500))
    ## picture to be determined 

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Word english={} farsi={}>".format(self.english, self.farsi)



class Vocabulary(db.Model):
    """user vocab lists """

    __tablename__= "vocabs"

    id = db.Column(db.Integer, primary_key =True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    user = db.relationship('User', backref=db.backref('vocabs'))
    words = db.relationship('Word', secondary='vocab_words', backref=db.backref('vocabs'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Vocabs {} for {} | {} words>".format(self.vocab_id, self.user_id , len(self.words))


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
