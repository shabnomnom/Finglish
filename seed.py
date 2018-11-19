import random
from faker import Faker

from model import User, Word, Vocabulary, connect_to_db, db


def load_words():
    """load words data"""
    # printing the table?
    print("Words")
    Word.query.delete()

    with open("seed.data/vocabs.csv") as file:
        for row in file:
            row = row.rstrip()

            english, farsi_phonetic, farsi, _ = row.split(",")

            word = Word(english=english,
                        farsi_phonetic=farsi_phonetic, farsi=farsi)

            db.session.add(word)

    db.session.commit()


def create_vocabs(user_id):
    vocab = Vocabulary(user_id=user_id, lesson_num=1)
    word_count = Word.query.count()
    word_ids = random.choices([i for i in range(1, word_count)], k=20)
    for i in word_ids:
        word = Word.query.get(i)
        vocab.words.append(word)
    db.session.add(vocab)
    db.session.commit()


def load_users():
    """load users from u.user into database"""

    ## print user class
    print("Users")

    #delete before adding new user so you don't doplicate users data
    User.query.delete()
    fake = Faker()

    for _ in range(25):
        user = User(first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    password=fake.password(),
                    age=random.randint(18, 100),
                    country=fake.country())

        db.session.add(user)
        db.session.commit()

        create_vocabs(user.id)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)

    # Import different types of data
    load_words()
    load_users()
