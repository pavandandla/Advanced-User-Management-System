from flask import Blueprint
from controllers.user_controller import (
    signup,
    login,
    profile,
    logout,
    sent_email_passwordreset,
    update_password,
    update_email,
    create_post,
    get_post,
    create_comment,
    get_comment,
    update_post,
    delete_post,
    update_comment,
    delete_comment
    
)

# Blueprint for user authentication routes
user_bp = Blueprint('user_bp', __name__)

# Define routes
user_bp.route('/signup', methods=['POST'])(signup)
user_bp.route('/login', methods=['POST'])(login)
user_bp.route('/profile/<int:user_id>', methods=['GET'])(profile)
user_bp.route('/update-password', methods=['POST'])(update_password)
user_bp.route('/sent-email-passwordreset', methods=['POST'])(sent_email_passwordreset)
user_bp.route('/update-email/<int:user_id>', methods=['PATCH'])(update_email)
user_bp.route('/logout', methods=['POST'])(logout)
user_bp.route('/create-post', methods=['POST'])(create_post)
user_bp.route('/get-post', methods=['GET'])(get_post)
user_bp.route('/update-post/<int:post_id>', methods=['PUT'])(update_post)
user_bp.route('/delete-post/<int:post_id>', methods=['DELETE'])(delete_post)
user_bp.route('/create-comment', methods=['POST'])(create_comment)
user_bp.route('/get-comment', methods=['GET'])(get_comment)
user_bp.route('/update-comment/<int:comment_id>', methods=['PUT'])(update_comment)
user_bp.route('/delete-comment/<int:comment_id>', methods=['DELETE'])(delete_comment)