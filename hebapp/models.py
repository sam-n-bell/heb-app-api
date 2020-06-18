# from hebapp import db
# from datetime import datetime


# class User(db.Model):
#     __tablename__ = 'users'
#     user_id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.Text, unique=False, nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#     jwts = db.relationship('User_Jwt', backref="user", lazy=True)

# class User_Jwt(db.Model):
#     __tablename__ = 'user_jwts'
#     user_jwt_id = db.Column(db.Integer, primary_key=True)
#     jwt = db.Column(db.Text, nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
