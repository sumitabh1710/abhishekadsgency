from flask import request, jsonify
from models import db, Comment, User
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

def postComment(review_id):
    try:
        data = request.json

        userId = data.get('user_id')
        reviewId = review_id
        text = data.get('text')

        new_Comment = Comment(user_id=userId, review_id=reviewId, text=text)

        db.session.add(new_Comment)
        db.session.commit()

        return jsonify({"message": "Comment Added successfully"}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def updateComment(review_id):
    try:
        data = request.json

        userId = data.get('user_id')
        reviewId = review_id
        text = data.get('text')
        current_timestamp = datetime.now()
        
        try:
            existing_review = Comment.query.filter_by(user_id=userId, review_id=reviewId).update(dict(text=text, post_date=current_timestamp))
            db.session.commit()
            return {'message': 'Comment updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def deleteComment(review_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    data = request.json
    userId = data.get('user_id')
    if user.user_id == userId:
        comment = Comment.query.filter_by(user_id=userId, review_id=review_id).first()

        if comment:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({'message': "Comment successfully deleted!"}), 200
        else:
            return jsonify({'message': "Comment not found!"}), 404
    else:
        return jsonify({'message': "You don't have access!"}), 401
        
    
