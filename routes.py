from flask.wrappers import Response
from flask import request, abort, jsonify, Blueprint

from models import User
from settings import X_SECRET_VALUE
from utils import create_new_user, list_of_users, update_user, delete_user


main = Blueprint("main", __name__)


@main.route("/api/users", methods=["POST", "GET"])
def get_or_create_users() -> Response:
    if request.method == "GET":
        return list_of_users()

    else:
        if request.headers.get("x-secret") != X_SECRET_VALUE:
            abort(400)
        return create_new_user(request)


@main.route("/api/users/<int:pk>", methods=["PUT", "GET", "DELETE"])
def get_user_and_create_or_delete(pk: int) -> Response:
    user = User.query.get(pk)
    if not user:
        abort(400)

    if request.method == "GET":
        return jsonify({"status_code": 200, "user": {"username": user.username, "email": user.email}})

    elif request.method == "PUT":
        return update_user(user, request)

    else:
        if request.headers.get("x-secret") != X_SECRET_VALUE:
            abort(400)
        return delete_user(user)


@main.route("/api")
def hello_world() -> Response:
    return jsonify({"data": "Hello, World!", "status_code": 200})
