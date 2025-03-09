import datetime
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from sqlalchemy import desc, func
from app.models import Cleanwalk, CleanwalkUser, db, User, Role, Organization
from app.utils import validate_api_key, hash_password, upload_img, send_reset_email
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError
from app.utils import verify_google_token
import uuid
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os

users_bp = Blueprint('users', __name__)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
RESET_PASSWORD_SALT = os.getenv("RESET_PASSWORD_SALT")

serializer = URLSafeTimedSerializer(JWT_SECRET_KEY)

@users_bp.before_request
def check_api_key():
    if request.method == 'OPTIONS':  # Handle preflight requests to enable CORS
        return
    
    api_key = request.headers.get('X-API-Key')  # Get the API key from the header
    
    # Verify the API key
    if not validate_api_key(api_key):
        return jsonify({'message': 'Invalid API KEY'}), 401

# Secure routes

#------------------------------------GET------------------------------------#

# Route to get user by id
@users_bp.route('/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.query(User, Role).join(Role, User.role_id == Role.id).filter(User.id == user_id).first()

    if user:
        user_data = {
            'id': user.User.id,
            'name': user.User.name,
            'email': user.User.email,
            'created_at': user.User.created_at,
            'profile_picture': user.User.profile_picture,
            'role': user.Role.role
        }
        print(user_data)
        return jsonify(user_data)
    else:
        print("User not found")
        return jsonify({'message': 'User not found'}), 404
    
# Route to get association by user id
@users_bp.route('/association/<string:user_id>', methods=['GET'])
def get_association(user_id):
    user = db.session.query(User, Organization).join(Organization, User.id == Organization.user_id).filter(User.id == user_id).first()

    if user:
        user_data = {
            'id': user.User.id,
            'name': user.User.name,
            'email': user.User.email,
            'description': user.Organization.description,
            'web_site': user.Organization.web_site,
            'social_medias': user.Organization.social_medias,
            'banner_img': user.Organization.banner_img,
            'profile_picture': user.User.profile_picture,
            'role': user.User.role_id
        }
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404
    
# Route to get associations ordered by RAND
@users_bp.route('/associations', methods=['GET'])
def get_organizations():
    organizations = db.session.query(User, Organization).join(Organization, User.id == Organization.user_id).filter(User.role_id == 2).order_by(func.rand()).all()
    if organizations:
        organization_data = []
        for organization in organizations:
            organization_data.append({
                'id': organization.User.id,
                'name': organization.User.name,
                'email': organization.User.email,
                'description': organization.Organization.description,
                'web_site': organization.Organization.web_site,
                'social_medias': organization.Organization.social_medias,
                'banner_img': organization.Organization.banner_img,
                'profile_picture': organization.User.profile_picture
            })
        return jsonify(organization_data)
    else:
        return jsonify({'message': 'Organizations not found'}), 404

# Route to get all users
@users_bp.route('', methods=['GET'])
def get_all_users():
    users = db.session.query(User, Role).join(Role, User.role_id == Role.id)
    if users:
        user_data = []
        for user in users:
            user_data.append({
                'id': user.User.id,
                'name': user.User.name,
                'email': user.User.email,
                'created_at': user.User.created_at,
                'profile_picture': user.User.profile_picture,
                'role': user.Role.role
            })
        return jsonify(user_data)
    else:
        return jsonify({'message': 'Users not found'}), 404

#------------------------------------DELETE------------------------------------#

# Route to delete user by id
@users_bp.route('/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    # Check if user is an association
    association = Organization.query.filter_by(user_id=user_id).first()
    # Anonymize the user
    if association:
        association.description = None
        association.web_site = None
        association.social_medias = None
        association.banner_img = None
        db.session.commit()
    if user:
        user.name = "Deleted User"
        user.email = f"deleted_user_{user_id}@example.com"
        user.google_id = None  # Or an anonymous value if necessary
        user.profile_picture = None
        db.session.commit()

#------------------------------------POST------------------------------------#

# Login route
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from the request
    print(data)

    email = data.get('email')
    res = db.session.query(User, Role).join(Role, User.role_id == Role.id).filter(User.email == email).first()
    if res:
        if res.User.password == hash_password(data.get('password'), res.User.salt):
            access_token = create_access_token(identity=res.User.id, additional_claims={'role': res.Role.role})
            return jsonify({
                'message': 'Successful connection', 
                'id': res.User.id, 'email': email, 
                'name': res.User.name,
                'profile_picture': res.User.profile_picture, 
                'access_token': access_token,
                'role': res.Role.role
            }), 200
        else:
            return jsonify({'message': 'Username or password incorrect'}), 401
    else:
        print("Unknown email address")
        return jsonify({'message': 'Unknown email address'}), 404
    
# Google login route
@users_bp.route('/google-login', methods=['POST'])
def google_login():
    data = request.get_json()
    required_keys = ['token']
    if not all(key in data for key in required_keys):
        return jsonify({'message': 'Request body is incomplete'}), 400

    # Use helper to verify the token
    user_info = verify_google_token(data['token'])  # Returns user info if the token is valid

    if user_info:
        # Search for the user in the database
        user_role = db.session.query(User, Role).join(Role, User.role_id == Role.id).filter(User.email == user_info['email']).first()

        # If the user does not exist, create a new user account
        if not user_role:
            # Check if role_id is provided, otherwise use a default role (e.g., 1)
            role_id = data.get('role_id', 1)

            if role_id == 2:  # If association
                profile_picture = user_info.get('picture')
            else:
                profile_picture = "https://api.dicebear.com/8.x/fun-emoji/svg?seed=" + str(uuid.uuid4())
                
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                profile_picture=profile_picture,
                role_id=role_id,
                created_at=datetime.datetime.now()
            )
            db.session.add(user)
            db.session.commit()

            # Search again to get the User object with the role
            user_role = db.session.query(User, Role).join(Role, User.role_id == Role.id).filter(User.email == user_info['email']).first()

        user, role = user_role
        role_name = 'association' if role.id == 2 else 'user'

        # Generate a JWT token for the user (if using flask_jwt_extended)
        access_token = create_access_token(identity=user.id, additional_claims={'role': role_name})

        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'profile_picture': user.profile_picture,
                'role': role_name
            }
        })

    else:
        return jsonify({'error': 'Invalid token'}), 400

# Login with token route
@users_bp.route('/token-login', methods=['POST'])
@jwt_required()
def tokenLogin():
    current_user = get_jwt_identity()
    claims = get_jwt()

    if current_user:
        res = db.session.query(User, Role).join(Role, User.role_id == Role.id).filter(User.id == current_user).first()
        return jsonify({
            'message': 'Successful connection', 
            'id': res.User.id, 
            'email': res.User.email, 
            'name': res.User.name,
            'profile_picture': res.User.profile_picture, 
            "role": claims["role"]
        }), 200
    else:
        return jsonify({'message': 'Invalid token'}), 401

# Route for creating a new user
@users_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)  # Get JSON data from the request
    if not data:
        return jsonify({'message': 'Request body is empty or not a valid JSON'}), 400

    required_keys = ['name', 'email', 'password', 'role_id']
    if not all(key in data for key in required_keys):
        return jsonify({'message': 'Request body is incomplete'}), 400

    # Extract user data from the request JSON
    name = data.get('name')
    email = data.get('email')
    profile_picture = data.get('profile_picture')
    salt = os.urandom(16)
    password = hash_password(data.get('password'), salt)
    role_id = data.get('role_id')
    
    try:
        # Try to create the new user
        new_user = User(
            name=name,
            email=email,
            profile_picture=profile_picture,
            password=password,
            salt=salt,
            role_id=role_id,
            created_at=datetime.datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()

        if role_id == 2:  # If the user is an organization, create association table
            new_association = Organization(user_id=new_user.id)
            db.session.add(new_association)
            db.session.commit()

        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

    except IntegrityError as e:
        print(e, "ErrorIntegrity")
        # Handle integrity error (duplicate email address)
        db.session.rollback()  # Rollback the transaction
        return jsonify({'message': 'Email address already in use'}), 400

#------------------------------------PUT------------------------------------#

# Route for updating user by id
@users_bp.route('/<string:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()

        # Update user data from the request JSON
        user.name = data.get('name', user.name)
        user.profile_picture = data.get('profile_picture', user.profile_picture)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404
    
# Route for updating user password by id
@users_bp.route('/password/<string:user_id>', methods=['PUT'])
@jwt_required()
def update_user_password(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        # Check if the old password is correct
        if user.password == hash_password(data.get('old_password'), user.salt):
            # Update user password
            user.password = hash_password(data.get('new_password'), user.salt)
            db.session.commit()
            return jsonify({'message': 'Password updated successfully'})
        else:
            return jsonify({'message': 'Old password is incorrect'}), 400
        
# Route for updating association by user id
@users_bp.route('/association/<string:user_id>', methods=['PUT'])
@jwt_required()
def update_association(user_id):
    # Retrieve the user
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Check if the user is an organization
    association = Organization.query.filter_by(user_id=user_id).first()
    
    if not association:
        return jsonify({'message': 'Association not found'}), 404

    # Get data from the request JSON
    data = request.get_json()
    
    # Update association fields if provided
    association.description = data.get('description', association.description)
    association.web_site = data.get('web_site', association.web_site)
    association.social_medias = data.get('social_medias', association.social_medias)
    association.banner_img = data.get('banner_img', association.banner_img)
    
    # Update user fields if provided
    user.profile_picture = data.get('profile_picture', user.profile_picture)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Association updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update association', 'error': str(e)}), 500
    
# Route to send reset password email
@users_bp.route('/send-reset-email', methods=['POST'])
def send_reset_email_route():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email required'}), 400

    try:
        # Send reset email
        send_reset_email(email)
        return jsonify({'message': 'Reset email sent'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to reset password with token
@users_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        # Load email from token
        email = serializer.loads(token, salt=RESET_PASSWORD_SALT, max_age=1200)  # 20 minutes
    except SignatureExpired:
        return jsonify({'message': 'The reset link has expired.'}), 400
    except BadSignature:
        return jsonify({'message': 'Invalid reset link.'}), 400

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Get the new password from the request
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'error': 'New password required'}), 400

    # Generate a new salt and hash the password
    salt = os.urandom(16)
    hashed_password = hash_password(new_password, salt)

    # Update the user with the new password
    user.password = hashed_password
    user.salt = salt

    try:
        # Commit changes to the database
        db.session.commit()
        return jsonify({'message': 'Password reset successfully'}), 200
    except Exception as e:
        # Rollback in case of error to avoid leaving the database in an inconsistent state
        db.session.rollback()
        return jsonify({'message': 'Error updating password', 'error': str(e)}), 500
