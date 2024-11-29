from flask import Blueprint
from controllers.user_controller import (
    signup, 
    login, 
    delete_user, 
    get_userdata, 
    patch_user, 
    update_user , 
    update_post,
    delete_post,
    update_comment,
    delete_comment
)
# Blueprint for user authentication routes
admin_bp = Blueprint('admin_bp', __name__)

# Define routes
admin_bp.route('/signup', methods=['POST'])(signup)
admin_bp.route('/login', methods=['POST'])(login)
admin_bp.route('/delete-user/<int:user_id>', methods=['DELETE'])(delete_user)
admin_bp.route('/get-userdata', methods=['GET'])(get_userdata)
admin_bp.route('/patch-user/<int:user_id>', methods=['PATCH'])(patch_user)
admin_bp.route('/update-post/<int:post_id>', methods=['PUT'])(update_post)
admin_bp.route('/delete-post/<int:post_id>', methods=['DELETE'])(delete_post)
admin_bp.route('/update-user/<int:user_id>', methods=['PUT'])(update_user)
admin_bp.route('/update-comment/<int:comment_id>', methods=['PUT'])(update_comment)
admin_bp.route('/delete-comment/<int:comment_id>', methods=['DELETE'])(delete_comment)

