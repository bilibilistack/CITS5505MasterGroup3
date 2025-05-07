from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.models import User 
from app.models import Share
from app.models import db
import json

# Create a Blueprint for the share module to organize routes
share_bp = Blueprint('share', __name__)

# User fuzzy search route
@share_bp.route('/search_users', methods=['GET'])
def search_users():
    """
    find users list
    """
    # Retrieve the search term and current user from the GET request
    search_term = request.args.get('searchTerm')  
    currentusername = session.get('username')

    # Apply a case-insensitive search for usernames containing the search term
    # Also, exclude the current user from the results
    users = User.query.filter(User.username.ilike(f'%{search_term}%')) \
        .filter(User.username != currentusername)  # Exclude the current user from search results
    
    # Prepare the result as a list of dictionaries containing the user ID and username
    result = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(result)  



@share_bp.route('/share_data', methods=['POST'])
def share_data():
    """
    share date to other users.
    """
    # get data and user id from front
    selected_users = request.json.get('selectedUsers')
    content = request.json.get('content')
    currentuserid = session.get('user_id')
    urlparams=request.json.get('urlParams')

    # check if there any data in select
    if not selected_users or not content:
        return jsonify({"success": False, "message": "No users selected or content missing."}), 400

    # make sure current user do the share action
    if currentuserid not in selected_users:
        selected_users.append(currentuserid) 

    # save share record
    for user_id in selected_users:
        if user_id != currentuserid:  
            share = Share(content=content, weatherdata=json.dumps(urlparams), shared_by=currentuserid, shared_to=user_id)
            db.session.add(share)

    db.session.commit()
    return jsonify({"success": True, "message": "Data shared successfully."}), 200

def get_shares_for_user():
    """
    get share record   
    """
    
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    shares = Share.query.filter_by(shared_to=user_id).all()

    return shares