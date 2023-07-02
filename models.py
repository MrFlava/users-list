from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
# from itsdangerous import Serializer, BadSignature, SignatureExpired

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # def generate_auth_token(self,):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     return s.dumps({'id': self.id})

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None    # valid token, but expired
    #     except BadSignature:
    #         return None    # invalid token
    #     user = User.query.get(data['id'])
    #     return user
