from models.all_models import User, db, Post, Comment
from flask import current_app
from flask import request
import jwt
from config.config import bcrypt
from flask_mail import Message
from config.config import mail
from itsdangerous import URLSafeTimedSerializer as Serializer
import os
from dotenv import load_dotenv 


def signup(data):#,user_ifo
    try:
        if "username" in data and "email" in data and "password" in data:
            username = data["username"]
            email = data["email"]
            password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

            role = data.get("role", "user")  # Defaults to 'user' if 'role' is not provided
            
            
            # Create a new user object
            new_user = User(username=username, email=email, password=password,role=role)  # Hash password before saving!
            
            db.session.add(new_user)
            db.session.commit()
            return {'status': "success", "statusCode": 201, "message": "User created successfully!"}, 201
        else:
            return {'status': "failed", "statusCode": 400, "message": "Username, email, and password are required"}, 400
    except Exception as e:
        db.session.rollback()
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500
    
def login(data):
    try:
        if "email" in data and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if user and bcrypt.check_password_hash(user.password, data["password"]):
                # Include role and username in the token
                token_Data = {
                    'role': user.role,
                    'username': user.username,
                    'id': user.id
                }
                #print("id===>",user.id)
                
                # Encode the token using JWT
                token = jwt.encode(token_Data, str(os.getenv('SECRET_KEY')) , algorithm='HS256')

                print("token===>",token)
               
                return {'message':f"Login Successful.Welcome,{user.username}!", 'status': "success", "statusCode": 200, "token": token}, 200
            else:
                return {'status': "failed", "statusCode": 401, "message": "Invalid credentials!"}, 401
        else:
            return {'status': "failed", "statusCode": 400, "message": "Email and password are required"}, 400
    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500

    
def profile(user_id):
    try:
        user = User.query.get_or_404(user_id)
        if user:
            user_Data = {
                 "id":user.id,
                 "username": user.username,
                 "email": user.email,
                 "hashpassword":user.password
                }
            return {'status': "success", "statusCode": 200, "message": "User profile found", "data": user_Data}, 200
        else:
            return {'status': "failed", "statusCode": 404, "message": "User not found"}, 404
    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500

def update_email(user_id,data):
    try:
        user = User.query.get_or_404(user_id)
        if user:
            new_Email=data['new_Email']
            if User.query.filter_by(email=new_Email).first():
               return {'status': "failed", "statusCode": 400, "message": "New email is already in use"}, 400
            else:
                user.email=new_Email
                db.session.commit()
                return {'status': "success", "statusCode": 200, "message": "Email updated successfully", "data": {"new_Email":user.email}}, 200
        else:
            return {'status': "failed", "statusCode": 404, "message": "User not found"}, 404
        
    except Exception as e:
        db.session.rollback()
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500

def sent_email_passwordreset(data):
    try:
        if "email" not in data:
            return {'status': "failed", "statusCode": 400, "message": "Email is required"}, 400

        email = data["email"]
        existing_user = User.query.filter_by(email=email).first()

        if not existing_user:
            return {'status': "failed", "statusCode": 404, "message": "User not found"}, 404

        serializer = Serializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps({'email': email})

        msg = Message(
            subject='Password Update Request',
            recipients=[email],
            html=f'''
                <p>Hello {email},</p>
                <p>This is a test email sent from Flask-Mail!</p>
                <p>Please follow the link below to update your password:</p>
                <a href="http://localhost:5000/update_password/{token}">Update Password</a>
            '''
        )

        mail.send(msg)
        return {'status': "success", "statusCode": 200, "message": "Email sent successfully"}, 200
    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500

def update_password(token, data):
    try:
        serializer = Serializer(current_app.config['SECRET_KEY'])
        token_Data = serializer.loads(token, max_age=600)
        email = token_Data['email']

        if "new_Password" not in data:
            return {'status': "failed", "statusCode": 400, "message": "New password is required"}, 400

        new_Password = data["new_Password"]
        user = User.query.filter_by(email=email).first()

        if not user:
            return {'status': "failed", "statusCode": 404, "message": "User not found"}, 404

        user.password = bcrypt.generate_password_hash(new_Password).decode('utf-8')
        db.session.commit()
        return {'status': "success", "statusCode": 200, "message": "Password updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500




def delete_user(user_id):
    """
    Deletes a user from the database.
    """
    try:
        user = User.query.get_or_404(user_id)  # Retrieve user by ID or return 404 if not found
        db.session.delete(user)  # Delete the user from the session
        db.session.commit()  # Commit the changes to the database
        return {'status': "success", "statusCode": 200, "message": "User deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        return {'status': "failed", "statusCode": 500, "message": "Error deleting user", "error": str(e)}, 500

def get_userdata():
    try:
        users = User.query.all()  # Retrieve  user
        
        if not users:
            return {'status': "failed", "statusCode": 404, "message": "No users found"}, 404  # Handle no users case

        # Prepare user data for response
        user_data = [{'username': user.username, 'email': user.email, 'role': user.role} for user in users]
        
        return {'status': "success", "statusCode": 200, "data": user_data}, 200  # Return user data as JSON
    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error retrieving user data", "error": str(e)}, 500


def patch_user(user_id, data):
    try:
        user = User.query.get_or_404(user_id)
        
        if 'username' in data:
            user.username = data.get('username')
        if 'email' in data:
            user.email = data.get('email')
        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

        db.session.commit()
        return {'status': "success", "statusCode": 200, "message": "User updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {'status': "failed", "statusCode": 500, "message": "Error updating user", "error": str(e)}, 500


def update_user(user_id, data):
    try:
        user = User.query.get_or_404(user_id)
        
        if 'username' in data:
            user.username = data.get('username')
        if 'email' in data:
            user.email = data.get('email')
        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

        db.session.commit()
        return {'status': "success", "statusCode": 200, "message": "User updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {'status': "failed", "statusCode": 500, "message": "Error updating user", "error": str(e)}, 500
    
# @log_function_execution
def logout(user_info):
    try:
        # Normally, the frontend will handle removing the JWT token.
        return {'status': "success", "statusCode": 200, "message": "Logged out successfully!"}, 200
    except Exception as e:
        return {'status': "failed", "statusCode": 500, "message": "Error occurred", "error": str(e)}, 500
    
#task 6:related work

def create_post(current_user,data):
    user = User.query.filter_by(id=current_user.id).first()
    if not user:
        return {'status': "failed", "statusCode": 404, "message": "No users found"}, 404  # Handle no users case
    else:
        if Post.query.filter_by(title=data['title']).first():
            return {'status': "failed", "statusCode": 400, "message": "Title is already in use"}, 400
        else:
            new_post = Post(title=data['title'], content=data['content'], owner=user)
            db.session.add(new_post)
            db.session.commit()
            return {'status': "success", "statusCode": 201, "message": "Post created successfully"}, 201
   
# Get all posts
def get_post(current_user):
    user = User.query.filter_by(id=current_user.id).first()
    user_id=user.id
    post = Post.query.filter_by(owner_id=user_id).first()
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "Posts not found"}, 404 
    
    comments = Comment.query.filter_by(post_id=post.id).all()
    return {
        'status': "success",
        "statusCode": 200,
        "message":"See the posts ",
        "data": {"id": post.id,
        "title": post.title,
        "content": post.content,
        "comments": [{"id": comment.id, "content": comment.comment} for comment in comments]}
    }, 200

def update_post(post_id,data):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "Posts not found"}, 404 
    
    if Post.query.filter_by(title=data['title']).first():
            return {'status': "failed", "statusCode": 400, "message": "Title is already in use"}, 400
    else:
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        return  {'status': "success", "statusCode": 200, "message": "Post updated successfully"}, 200
    

def delete_post(post_id):
    """
    Deletes a post from the database.
    """
    try:
        post = Post.query.get_or_404(post_id)  # Retrieve post by ID or return 404 if not found
        db.session.delete(post)  # Delete the post from the session
        db.session.commit()  # Commit the changes to the database
        return {'status': "success", "statusCode": 200, "message": "Post deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        return {'status': "failed", "statusCode": 500, "message": "Error deleting post", "error": str(e)}, 500
    

def create_comment(current_user,data):
    user = User.query.filter_by(id=current_user.id).first()
    user_id=user.id
    post = Post.query.filter_by(owner_id=user_id).first()
    
    if not post:
        return {'status': "failed", "statusCode": 404, "message": "No users found"}, 404  # Handle no users case
    
    new_comment = Comment(comment=data['comment'], user=user, post=post)
    db.session.add(new_comment)
    db.session.commit()
    return {'status': "success", "statusCode": 201, "message": "Comment created successfully"}, 201

def get_comment(current_user):
    comments = Comment.query.all()
    output = []
    for comment in comments:
        comment_data = {
            'id': comment.id,
            'comment': comment.comment,
            'post_id': comment.post.id,
            'user_id': comment.user.id
        }
        output.append(comment_data)
    return {'status': "success", "statusCode": 200, "message": "All comments", "data": output}, 200

def update_comment(comment_id, data):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return {'status': "failed", "statusCode": 404, "message": "Comment not found"}, 404
    
    comment.comment = data['comment']
    db.session.commit()
    
    return {'status': "success", "message": "Comment updated successfully"}, 200

def delete_comment(current_user, comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return {'status': "failed", "statusCode": 404, "message": "Comment not found"}, 404
    db.session.delete(comment)
    db.session.commit()
    return {'status': "success", "message": "Comment updated successfully"}, 200


