from flask import Blueprint, request, jsonify
from app.models import User 
from app.models import Share
from app.models import db

# Create a Blueprint for the share module to organize routes
share_bp = Blueprint('share', __name__)

# User fuzzy search route
@share_bp.route('/search_users', methods=['GET'])
def search_users():
    # Retrieve the search term and current user from the GET request
    search_term = request.args.get('searchTerm')  
    currentUser = request.args.get('currentUser') 

    # Apply a case-insensitive search for usernames containing the search term
    # Also, exclude the current user from the results
    users = User.query.filter(User.username.ilike(f'%{search_term}%')) \
        .filter(User.username != currentUser)  # Exclude the current user from search results
    
    # Prepare the result as a list of dictionaries containing the user ID and username
    result = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(result)  



@share_bp.route('/share_data', methods=['POST'])
def share_data():
    # get data and user id from front
    selected_users = request.json.get('selectedUsers')
    content = request.json.get('content')
    current_user = request.json.get('currentUser') 

    # check if there any data in select
    if not selected_users or not content:
        return jsonify({"success": False, "message": "No users selected or content missing."}), 400

    # make sure current user do the share action
    if current_user not in selected_users:
        selected_users.append(current_user) 

    # save share record
    for user_id in selected_users:
        if user_id != current_user:  
            share = Share(content=content, shared_by=current_user, shared_to=user_id)
            db.session.add(share)

    db.session.commit()
    return jsonify({"success": True, "message": "Data shared successfully."}), 200
