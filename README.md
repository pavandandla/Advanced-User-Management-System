# **Advanced User Management System**

## **Description**

The **Advanced User Management and Role-Based API** is a robust Flask-based application that integrates **user authentication**, **role-based access control (RBAC)**, and **data management** features. The system supports **password reset** and **forgot password** functionality with secure token-based email verification. It implements **CRUD operations** on user records with **JWT authentication** and **SQLAlchemy ORM** for database interactions, including managing relationships between tables such as **users**, **posts**, and **comments**.



## **Features**

- **Secure Authentication and Authorization**: Uses JWT for secure token-based user authentication and implements role-based access control (RBAC).
- **Efficient Database Operations**: CRUD operations for users, posts, and comments, utilizing SQLAlchemy for efficient database interactions.
- **Email Functionality**: Password reset, forgot password functionality, and secure token-based email verification.
- **Environment Configuration**: Manage environment settings securely with **python-dotenv** for flexibility in different environments.
- **Modular Code Organization**: Maintainable project structure with separate modules for user authentication, roles, and CRUD operations.
- **Standardized API Responses**: Consistent response formatting across all API endpoints.
- **Comprehensive Error Handling**: Proper error responses for common issues such as authentication errors, authorization failures, and invalid inputs.


## Prerequisites

- Python 3.9+
- pip
- Virtual environment support
## **Libraries Used**

- **Flask** 
- **Flask-SQLAlchemy** 
- **JWT** 
- **Flask-Mail** 
- **python-dotenv** 
- **Werkzeug** 
- **Bcrypt** 



## **Installation and Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/pavandandla/Advanced-User-Management-System.git
cd Advanced-User-Management-System
```



### **2. Create a Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```



### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```



### **4. Configure Environment Variables**

Create a `.env` file in the root directory with the following configuration:

```plaintext
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./test.db  # Or MySQL connection string
JWT_SECRET_KEY=your_jwt_secret_key
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
FLASK_ENV=development
```

- **SECRET_KEY**: Key for signing cookies and sessions.
- **DATABASE_URL**: SQLite or MySQL connection string for storing user data.
- **JWT_SECRET_KEY**: Secret key used for encoding JWT tokens.
- **MAIL_USERNAME**: Email address used to send reset and verification emails.
- **MAIL_PASSWORD**: Password for the email account used for sending emails.
- **FLASK_ENV**: Set to `development` for debugging.



### **5. Set Up the Database**

Run the following command to initialize the database and create necessary tables:

```bash
python src/init_db.py
```



### **6. Run the Application**

To run the Flask application:

```bash
flask run
```

The application will be available at: `http://127.0.0.1:5000`





## **Example Workflow**

1. **User Registration**  
    To register a new user, users can make a `POST` request to `/register` with their details. The system will hash the password securely and store the user in the database.
    
2. **User Login**  
    To log in, users can make a `POST` request to `/login` with their credentials. If valid, the system will generate and return a JWT token for further authentication.
    
3. **Password Reset**  
    To reset their password, users can send a `POST` request to `/forgot-password` with their registered email address. A secure token will be sent via email. The user can then reset their password by sending a `POST` request to `/reset-password` with the token and new password.
    
4. **User Management**  
    Authorized users can perform CRUD operations on user records by accessing the `/user/<user_id>` route with appropriate HTTP methods (GET, PUT, DELETE).
    





## **Environment Configuration**

Example `.env` file:

```plaintext
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./test.db
JWT_SECRET_KEY=your_jwt_secret_key
```


## **Contact**

For questions, suggestions, or issues, contact:

- GitHub: [pavandandla](https://github.com/pavandandla)
