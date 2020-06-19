from hebapp import db, ma
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow import Schema, fields
from citext import CIText

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(CIText(), unique=True, nullable=False)
    first_name = db.Column(CIText(), nullable=False)
    password = db.Column(CIText(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    jwts = db.relationship('UserJwt', backref="user", lazy=True)

    def __repr__(self):
        return f'User({self.user_id}, {self.email}, {self.password}, {self.date_created})'

class UserJwt(db.Model):
    __tablename__ = 'user_jwts'
    user_jwt_id = db.Column(db.Integer, primary_key=True)
    jwt = db.Column(CIText(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

    def __repr__(self):
        return f'UserJwt({self.user_jwt_id}, {self.jwt}, {self.date_created}, {self.user_id})'


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = (
            "user_id",
            "email",
            "date_created",
            "first_name"
        )

class UserJwtSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = (
            "user_jwt_id",
            "jwt",
            "date_created",
            "user_id"
        )

class RegistrationSchema(Schema):
    email = fields.Email(required=True)
    first_name = fields.String(required=True, validate=Length(min=1, max=20))
    password = fields.Str(required=True, validate=Length(min=8, max=30))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=8, max=30))