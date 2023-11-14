from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

# Book Model
class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)

#Role Model
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

# User Model
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    #relationship
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

# Review Model
class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    rating = db.Column(db.Integer,CheckConstraint('rating >= 1 AND rating <= 5'))
    text = db.Column(db.String(1000))
    post_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    #relationships
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    book = db.relationship('Book', backref=db.backref('reviews', lazy=True))

# Comment Model
class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.review_id'), nullable=False)
    text = db.Column(db.String(1000))
    post_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    #relationships
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    review = db.relationship('Review', backref=db.backref('comments', lazy=True))