# app/routes/user_routes.py

from flask import Blueprint, request, jsonify
from models.user import User

user_bp = Blueprint('user', __name__)

# Route to register a new user
# tested successfully
@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')  # Extract email from request data

    # Check if a user with the provided email already exists
    existing_user = User.get_by_email(email)
    if existing_user:
        return jsonify({'message': 'User with this email already exists. Please register with a different email.'}), 400

    # If user with provided email doesn't exist, proceed with registration
    new_user = User(**data)
    new_user.save()
    return jsonify({'message': 'User registered successfully'}), 201

@user_bp.route('/user/<email>', methods=['GET'])
def get_user(email):
    user = User.get_by_email(email)
    if user:
        # Remove the password field before returning the user
        user.pop('password', None)
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Route to login a user
# tested successfully
@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if User.login(email, password):
        user = User.get_by_email(email)
        user_obj = User(**user)


        user_obj.log_in()
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# Route to delete a user
# tested successfully
@user_bp.route('/user/<email>', methods=['DELETE'])
def delete_user(email):
    if User.delete(email):
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Route to log out a user
# tested successfully
@user_bp.route('/logout/<email>', methods=['POST'])
def logout_user(email):
    user = User.get_by_email(email)

    if user:
        user_obj = User(**user)


        user_obj.log_out()
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
