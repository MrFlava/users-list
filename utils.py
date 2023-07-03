from flask import abort, jsonify
from flask.wrappers import Response, Request
from email_validator import validate_email, EmailNotValidError

from models import User, db


def list_of_users() -> Response:
    user_objects = User.query.all()
    users = []

    for user in user_objects:
        users.append({"username": user.username, "email": user.email})

    return jsonify({"users": users, "status_code": 200})


def create_new_user(request: Request) -> Response:
    username = request.json.get("username")
    email = ""
    try:
        emailinfo = validate_email(request.json.get("email"), check_deliverability=False)
        email = emailinfo.normalized

    except EmailNotValidError as e:
        abort(400)

    # email =
    password = request.json.get("password")

    if username is None or password is None or email is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user

    user = User(username=username, email=email)
    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"status_code": 201, "user": {"username": user.username, "email": user.email}})


def update_user(user: User, request: Request) -> Response:
    user.username = request.json.get("username")
    try:
        emailinfo = validate_email(request.json.get("email"), check_deliverability=False)
        user.email = emailinfo.normalized

    except EmailNotValidError as e:
        abort(400)
    user.hash_password(request.json.get("password"))

    db.session.commit()
    return jsonify({"status_code": 200, "user": {"username": user.username, "email": user.email}})


def delete_user(user: User) -> Response:
    db.session.delete(user)
    return jsonify({"data": "user were deleted", "status:code": 200})
