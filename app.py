from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from models import db, Role, User, Review, Comment
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from BooksService.booksService import postBook, getBooks, getBook, searchBookByAuthor, searchBookByGenre, searchBookByTitle
from RoleService.roleService import createRole
from ReviewService.reviewService import postReview, updateReview, deleteReview
from CommentService.commentService import postComment, updateComment, deleteComment
import secrets

app = Flask(__name__)

db_username = 'postgres'
db_password = 1234
db_host = 'localhost'
db_name = 'postgres'
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user_role = Role.query.filter_by(name='User').first()

    new_user = User(username=data['username'], password=hashed_password, role=user_role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role_id': user.role_id})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Login failed. Check your username and password.'}), 401

@app.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user.role.name == 'Admin':
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': "User Successfully deleted!"}), 200
    else:
        return jsonify({'message': "You don't have access!"}), 401
    
@app.route("/book", methods=['POST'])
def create_book():
    return postBook()

@app.route('/books', methods=['GET'])
def get_books():
    return getBooks()

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    return getBook(book_id)

@app.route('/search/<string:field>/<string:search_word>', methods=['GET'])
def search_books(field, search_word):
    if field == "title":
        return searchBookByTitle(search_word)
    elif field == "genre":
        return searchBookByGenre(search_word)
    elif field == "author":
        return searchBookByAuthor(search_word)
    return jsonify({'message': "Bad Request!"}), 400

@app.route('/role', methods=['POST'])
@jwt_required()
def create_role():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user.role.name == 'Admin':
        return createRole()
    else:
        return jsonify({'message': "You don't have access!"}), 401

@app.route('/review/<int:book_id>', methods=['POST'])
def post_review(book_id):
    return postReview(book_id)

@app.route('/review/<int:book_id>', methods=['PUT'])
def update_review(book_id):
    return updateReview(book_id)

@app.route('/review/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_review(book_id):
    try:
        return deleteReview(book_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/comment/<int:review_id>', methods=['POST'])
def post_comment(review_id):
    return postComment(review_id)

@app.route('/comment/<int:review_id>', methods=['PUT'])
def update_comment(review_id):
    try:
        return updateComment(review_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/comment/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(review_id):
    try:
        return deleteComment(review_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

