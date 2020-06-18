from hebapp.users.models import User, UserJwt, UserSchema

def serialize_many(users):
    user_schema = UserSchema()
    return user_schema.dump(users, many=True)


def return_marshmallow_schema_errors(errors):
    errors_str = ''
    for k, v in errors.items():
        errors_str += str(k)
        errors_str += ': '
        for error in v:
            errors_str += error
            errors_str += ' '
    return errors_str