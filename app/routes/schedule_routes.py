# routes/schedule_routes.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from models.schedule import Schedule
from models.user import User
from flask import request
schedule_bp = Blueprint('schedule', __name__)

# Route to create a new schedule
# tested successfully
@schedule_bp.route('/schedule', methods=['POST'])
def create_schedule():
    data = request.json
    user_email = data.get('email')  # Assuming the email is provided in the request data

    # Find the user by email
    user = User.get_id_by_email(user_email)
    if user:
        # Extract user_id from the user document
        user_id = user['_id']
        # Remove 'email' from data before passing to Schedule constructor
        data.pop('email', None)

        # Create a new schedule with user_id
        new_schedule = Schedule(user_id, **data)
        new_schedule.save()
        
        return jsonify({'message': 'Schedule created successfully'}), 201
    else:
        return jsonify({'message': 'User not found'}), 404

# Route to get all schedules for a user
# tested successfully
@schedule_bp.route('/schedules', methods=['GET'])
def get_all_schedules():
    # schedules = Schedule.get_all(user_id)
    user_email = request.args.get('email')
    user = User.get_id_by_email(user_email)
    if user:
        # Extract user_id from the user document
        user_id = user['_id']
        # condition type is present as well
        schedules = Schedule.get_all(user_id, type=request.args.get('type'))
        newschedules = [{**schedule, 'user_id': str(schedule['user_id']), '_id': str(schedule['_id'])} for schedule in schedules]


        return jsonify({'data': newschedules}), 200
        # Remove 'email' from data before passing to Schedule constructor

    return jsonify({'message': 'The user is not existing'}), 400

# Route to get a single schedule by ID for a user
# tested successfully
@schedule_bp.route('/schedule/<user_id>/<schedule_id>', methods=['GET'])
def get_schedule(user_id, schedule_id):
    user_id_obj = ObjectId(user_id)
    schedule_id_obj = ObjectId(schedule_id)
    schedules = Schedule.get_by_id(schedule_id_obj, user_id_obj)
    schedules['_id'] = str(schedules['_id'])
    schedules['user_id'] = str(schedules['user_id'])
    
    if not schedules:
        return jsonify({'message': 'Schedule not found'}), 404
    return jsonify(schedules), 200

# Route to update a schedule by ID for a user
# tested successfully
@schedule_bp.route('/schedule/<user_id>/<schedule_id>', methods=['PUT'])
def update_schedule(user_id, schedule_id):
    data = request.json
    updated_schedule = Schedule.update(schedule_id, user_id, **data)
    if not updated_schedule:
        return jsonify({'message': 'Schedule not found'}), 404
    return jsonify({'message': 'Schedule updated successfully'}), 200

# Route to delete a schedule by ID for a user
# tested successfully
@schedule_bp.route('/schedule/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    deleted_schedule = Schedule.delete(schedule_id)
    if not deleted_schedule:
        return jsonify({'message': 'Schedule not found'}), 404
    return jsonify({'message': 'Schedule deleted successfully'}), 200
