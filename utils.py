from flask import abort, jsonify
from flask.wrappers import Response, Request
from email_validator import validate_email, EmailNotValidError

from models import User, db


def email_validation(email: str) -> str:
    try:
        email_info = validate_email(email, check_deliverability=False)
        email = email_info.normalized
        return email

    except EmailNotValidError as e:
        abort(400)


def validate_required_fields(fields: list):
    if any(value is None for value in fields):
        abort(400)


def list_of_users() -> Response:
    user_objects = User.query.all()
    users = []

    for user in user_objects:
        users.append({"username": user.username, "email": user.email})

    return jsonify({"users": users, "status_code": 200})


def create_new_user(request: Request) -> Response:
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    validate_required_fields([username, email, password])

    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user

    validated_email = email_validation(email)

    user = User(username=username, email=validated_email)
    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"status_code": 201, "user": {"username": user.username, "email": user.email}})


def update_user(user: User, request: Request) -> Response:
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    validate_required_fields([username, email, password])

    user.username = username
    user.email = email_validation(email)
    user.hash_password(password)

    db.session.commit()
    return jsonify({"status_code": 200, "user": {"username": user.username, "email": user.email}})


def delete_user(user: User) -> Response:
    db.session.delete(user)
    return jsonify({"data": "user were deleted", "status:code": 200})
