from flask import Flask, abort, request, jsonify
from flask.wrappers import Response

from models import db, User
from utils import create_new_user, list_of_users, update_user, delete_user
from settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, X_SECRET_VALUE

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)


@app.route("/api/users", methods=["POST", "GET"])
def get_or_create_users() -> Response:
    if request.method == "GET":
        return list_of_users()

    else:
        if request.headers.get("x-secret") != X_SECRET_VALUE:
            abort(400)
        return create_new_user(request)


@app.route("/api/users/<int:pk>", methods=["PUT", "GET", "DELETE"])
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


@app.route("/api")
def hello_world() -> Response:
    return jsonify({"data": "Hello, World!", "status_code": 200})


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
