
from flask import request, Response, json, jsonify, g
from services import user_role_service
from middlewares import token_required, admin_required
from models.all_models import User, Post
# @authenticate_admin
def signup():
    #user_info = g.get('user_info')  # Extract user info if needed from middleware
    data = request.form
    response, status = user_role_service.signup(data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json') #mimetype='application/json'

def login():
    data = request.form
    response, status = user_role_service.login(data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

def profile(user_id):
    response, status = user_role_service.profile(user_id)
    return Response(response=json.dumps(response), status=status,mimetype='application/json')


def update_email(user_id):
    data=request.form
    response, status = user_role_service.update_email(user_id,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')


def sent_email_passwordreset():
    data = request.form
    response, status = user_role_service.sent_email_passwordreset(data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

def update_password():
    data = request.form
    response, status = user_role_service.update_password(data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@admin_required
def delete_user(current_user,user_id):
    """
    Deletes a user by ID after admin authentication.
    """
    response, status = user_role_service.delete_user(user_id)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')
  
@token_required
@admin_required
def get_userdata(current_user):
    #user_info = g.get('user_info')  # Authenticated user info
    #data = request.form
    response, status = user_role_service.get_userdata()
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@admin_required
def patch_user(current_user,user_id):
    # Authenticated user info
    data = request.form 
    response, status = user_role_service.patch_user(user_id,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@admin_required
def update_user(current_user,user_id):
    # Authenticated user info
    data = request.form
    response, status = user_role_service.update_user(user_id,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

def logout():
    user_info = g.get('user_info')  # Authenticated user info
    response, status = user_role_service.logout(user_info)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

# task:6 controllers
@token_required
def create_post(current_user):
    data = request.form
    response, status = user_role_service.create_post(current_user,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
def get_post(current_user):
    response, status = user_role_service.get_post(current_user)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@admin_required
def update_post(current_user,post_id):
    data=request.form
    response, status = user_role_service.update_post(post_id,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@admin_required
def delete_post(current_user, post_id):
    """
    Deletes a post by ID after user authentication.
    """
    # Call service to delete the post
    response, status = user_role_service.delete_post(post_id)  # Use post_id directly
    
    return Response(response=json.dumps(response), status=status, mimetype='application/json')


@token_required
def create_comment(current_user):
    data = request.form
    response, status = user_role_service.create_comment(current_user,data)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
def get_comment(current_user):
    response, status = user_role_service.get_comment(current_user)
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@admin_required
def update_comment(current_user, comment_id):
    # Authenticated user info
    data = request.form   
    response, status = user_role_service.update_comment(comment_id, data)  # Call service function
    return Response(response=json.dumps(response), status=status, mimetype='application/json')

@token_required
@admin_required
def delete_comment(current_user,comment_id):  
    response, status = user_role_service.delete_comment(current_user,comment_id)  # Use post.id
    return Response(response=json.dumps(response), status=status, mimetype='application/json')
