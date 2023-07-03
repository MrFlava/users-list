from flask import Flask

from models import db
from settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from routes import main


def create_app():
    new_app = Flask(__name__)
    new_app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    new_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    new_app.register_blueprint(main)
    db.init_app(new_app)

    return new_app


app = create_app()


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
