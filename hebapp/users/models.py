from hebapp import db, ma
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    jwts = db.relationship('UserJwt', backref="user", lazy=True)

    def __repr__(self):
        return f'User({self.user_id}, {self.email}, {self.password}, {self.date_created})'

class UserJwt(db.Model):
    __tablename__ = 'user_jwts'
    user_jwt_id = db.Column(db.Integer, primary_key=True)
    jwt = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

    def __repr__(self):
        return f'UserJwt({self.user_jwt_id}, {self.jwt}, {self.date_created}, {self.user_id})'


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = (
            "user_id",
            "email",
            "date_created"
        )

class UserJwtSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = (
            "user_jwt_id",
            "jwt",
            "date_created",
            "user_id"
        )