from config.database import db
from config.config import bcrypt

class User(db.Model):

    __tablename__ = 'User'  # Correct table name: 'User'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    # One-to-many relationship with Post
    posts = db.relationship('Post', backref='owner', cascade='all, delete-orphan', lazy=True)

    # One-to-many relationship with Comment
    comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan', lazy=True)


class Post(db.Model):
    __tablename__ = 'Post'  # Correct table name: 'Post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # ForeignKey with cascade on delete for User
    owner_id = db.Column(
        db.Integer, 
        db.ForeignKey('User.id', ondelete='CASCADE'),  # Corrected ForeignKey reference to 'User.id'
        nullable=False
    )

    # One-to-many relationship with Comment
    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy=True)


class Comment(db.Model):
    __tablename__ = 'Comment'  # Correct table name: 'Comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    
    # ForeignKey with cascade on delete for User
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('User.id', ondelete='CASCADE'),  # Corrected ForeignKey reference to 'User.id'
        nullable=False
    )
    
    # ForeignKey with cascade on delete for Post
    post_id = db.Column(
        db.Integer, 
        db.ForeignKey('Post.id', ondelete='CASCADE'),  # Corrected ForeignKey reference to 'Post.id'
        nullable=False
    )
