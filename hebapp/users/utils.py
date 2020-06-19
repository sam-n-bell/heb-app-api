from hebapp.users.models import User, UserJwt, UserSchema

def serialize_many(users):
    user_schema = UserSchema()
    return user_schema.dump(users, many=True)

def serialize_one(user):
    user_schema = UserSchema()
    return user_schema.dump(user, many=False)