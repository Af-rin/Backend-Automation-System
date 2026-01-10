from datetime import datetime, timedelta, timezone
from fastapi import status, Depends
from sqlalchemy import func
from app.helpers.utils.jwt_util import create_access_token
from app.models.user_model import UserModel
from app.helpers.schema_validations.auth_schema import authRegisterUsersRequest
from app.helpers.utils.password_hash import pwd_context
from sqlalchemy.orm import Session


async def register_user(data: authRegisterUsersRequest, db: Session):
    try:
        # Only admin can register 
        username = data.get('userName') or data.get('username') or data.get('user_name')
        email = data.get('email')
        password = data.get('password')
        register_token = data.get('registration_token')
        role = data.get("role")

        # check required field missing
        if not username or not email or not password or not register_token:
            response = {
                "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content":{
                    "error": True,
                    "data": {"message": "Invalid Credentials."},
                },
            }
            return response
        
        # check for user already exists
        user_exist = (
            db.query(UserModel)
            .filter(UserModel.user_name == username, UserModel.email == email, UserModel.role == role)
            .first()
        )
        if user_exist:
            response = {
                "status_code":status.HTTP_409_CONFLICT,
                "content":{
                    "error": True,
                    "data": {"message": "User already exists."},
                },
            }
            return response
        
        # create user
        user = UserModel(user_name=username, email=email, password=pwd_context.hash(password), role=role)
        db.add(user)
        db.commit()
        db.refresh(user)

        response = {
                "status_code":status.HTTP_201_CREATED,
                "content":{
                    "error": False,
                    "data": {
                        "user_id": str(user.id), 
                        "username": user.user_name, 
                        "message": "User created successfully!"
                    },
                },
        }
        return response
    except Exception as e:
        db.rollback()
        print(f"Error while registering user :: {str(e)}")
        response = {
                "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content":{
                    "error": True,
                    "data": {"message": "Internal server error while registering user."},
                },
            }
        return response


async def get_users_list(db: Session, page: int, items_per_page: int):
    try:
        # Note: role-based restriction (only admin can fetch all users) - handled in auth middleware
        offset = (page - 1) * items_per_page
        if offset<0:
            raise Exception("Pagination Offset cannot be negative")
        
        total = db.query(func.count(UserModel.id)).scalar()
        
        # Fetch all users
        users = (
            db.query(UserModel)
            .order_by(UserModel.created_at.desc())
            .offset(offset)
            .limit(items_per_page)
            .all()
        )

        if not users:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "error": True,
                    "data": {"message": "No users found."},
                },
            }
            return response

        # Convert to dicts (Beanie returns Document objects)
        user_list = [
            {
                "id": str(user.id),
                "username": user.user_name,
                "email": user.email,
                "role": user.role.value,
                "lastLogin": user.last_login.isoformat() if user.last_login else None,
                "createdAt": user.created_at.isoformat() if user.created_at else None,
            }
            for user in users
        ]

        response = {
            "status_code": status.HTTP_200_OK,
            "content": {
                "error": False,
                "data": {
                    "users": user_list, 
                    "pagination":{
                        "total": total,
                        "page": page,
                        "items_per_page": items_per_page,
                    },
                    "message": "Users fetched successfully."
                },
            },
        }
        return response

    except Exception as e:
        print(f"Error while fetching users :: {str(e)}")
        response = {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "content": {
                "error": True,
                "data": {"message": f"Internal server error while fetching users :: {str(e)}"},
            },
        }
        return response

async def login_user(data: dict, db: Session):
    try:
        username = data.get("username") or data.get("userName") or data.get('user_name')
        email = data.get("email")
        password = data.get("password")

        # Validate required fields
        if not username or not email or not password:
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "content": {
                    "error": True,
                    "data": {"message": "Invalid credentials."},
                },
            }

        # Fetch user
        user = (
            db.query(UserModel)
            .filter(UserModel.user_name == username, UserModel.email == email)
            .first()
        )

        if not user:
            return {
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "content": {
                    "error": True,
                    "data": {"message": "Invalid credentials."},
                },
            }

        # Verify password
        if not pwd_context.verify(password, user.password):
            return {
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "content": {
                    "error": True,
                    "data": {"message": "Invalid credentials."},
                },
            }

        # Generate JWT
        token_payload = {
            "sub": str(user.id),
            "username": user.user_name,
            "email": user.email,
            "role": user.role.value,
        }

        token, exp = create_access_token(token_payload)
        print(token, exp)

        # Update login metadata
        user.access_token = token
        user.last_login = datetime.now(timezone.utc)
        user.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

        return {
            "status_code": status.HTTP_200_OK,
            "content": {
                "error": False,
                "data": {
                    "access_token": token,
                    "token_type": "bearer",
                    "expires_in_utc": exp,
                },
            },
        }

    except Exception as e:
        db.rollback()
        print(f"Error while logging in :: {e}")

        return {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "content": {
                "error": True,
                "data": {"message": "Internal server error while logging in."},
            },
        }
    

async def get_user_profile(data: dict, db: Session):
    try:
        # Fetch current user profile
        user = (
            db.query(UserModel)
            .filter(UserModel.id == data.id)
            .first())

        if not user:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "error": True,
                    "data": {"message": "No user found."},
                },
            }
            return response

        # Convert to dicts (Beanie returns Document objects)
        user_list = {
                "id": str(user.id),
                "username": user.user_name,
                "email": user.email,
                "is_active": user.is_active,
                "lastLogin": user.last_login.isoformat() if user.last_login else None,
                "createdAt": user.created_at.isoformat() if user.created_at else None,
            }

        response = {
            "status_code": status.HTTP_200_OK,
            "content": {
                "error": False,
                "data": {"user": user_list},
            },
        }
        return response

    except Exception as e:
        print(f"Error while fetching me user :: {str(e)}")
        response = {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "content": {
                "error": True,
                "data": {"message": "Internal server error while fetching me user."},
            },
        }
        return response