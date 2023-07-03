from os import path

from flask import Flask, abort, request, jsonify, g, url_for

from models import User, db

basedir = path.abspath(path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/api/users', methods=['POST', 'GET'])
def new_user():
    if request.method == 'GET':
        user_objects = User.query.all()
        users = []

        for user in user_objects:
            users.append({'username': user.username, 'email': user.email})

        return jsonify({'users': users}, 200)

    else:
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')

        if username is None or password is None or email is None:
            abort(400)    # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(400)    # existing user

        user = User(username=username, email=email)
        user.hash_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', pk=user.id, _external=True)}


@app.route('/api/users/<int:pk>', methods=['PUT', 'GET', 'DELETE'])
def get_user(pk: int):
    user = User.query.get(pk)
    if not user:
        abort(400)

    if request.method == 'GET':
        return jsonify({'username': user.username, 'email': user.email}, 200)

    elif request.method == 'PUT':
        user.username = request.json.get('username')
        user.email = request.json.get('email')
        user.hash_password(request.json.get('password'))

        db.session.commit()
        return jsonify({'username': user.username, 'email': user.email}, 200)

    else:
        db.session.delete(user)
        return jsonify({'data': 'user were deleted'}, 200)


@app.route('/api')
def hello_world():
    return jsonify({'data': 'Hello, World!'})


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
