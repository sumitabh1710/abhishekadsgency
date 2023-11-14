from flask import request, jsonify
from models import db, Role

def createRole():
    try:
        data = request.json

        name = data.get('name')

        new_role = Role(name=name)

        db.session.add(new_role)
        db.session.commit()

        return jsonify({"message": "Role created successfully", "data": {"name": new_role.name}}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500