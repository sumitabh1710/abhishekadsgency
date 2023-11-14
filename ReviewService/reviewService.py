from flask import request, jsonify
from models import db, Review, User
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

def postReview(book_id):
    try:
        data = request.json

        userId = data.get('user_id')
        bookId = book_id
        rating = data.get('rating')
        text = data.get('text')
    
        new_review = Review(user_id=userId, book_id=bookId, rating=rating, text=text)

        db.session.add(new_review)
        db.session.commit()

        return jsonify({"message": "Review Added successfully"}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def updateReview(book_id):
    data = request.json

    userId = data.get('user_id')
    bookId = book_id
    rating = data.get('rating')
    text = data.get('text')
    current_timestamp = datetime.now()
        
    try:
        existing_review = Review.query.filter_by(user_id=userId, book_id=bookId).update(dict(rating=rating, text=text, post_date=current_timestamp))
        db.session.commit()
        return {'message': 'Review updated successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
    
def deleteReview(book_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    data = request.json
    userId = data.get('user_id')
    if user.user_id == userId:
        review = Review.query.filter_by(user_id=userId, book_id=book_id).first()

        if review:
            db.session.delete(review)
            db.session.commit()
            return jsonify({'message': "Review successfully deleted!"}), 200
        else:
            return jsonify({'message': "Review not found!"}), 404
    else:
        return jsonify({'message': "You don't have access!"}), 401
    
