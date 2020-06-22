def return_marshmallow_schema_errors(errors):
    """
    Returns all marshmallow validation errors in a single line string that's easier to read
    """
    errors_str = ''
    for k, v in errors.items():
        errors_str += str(k)
        errors_str += ': '
        for error in v:
            errors_str += error
            errors_str += ' '
    return errors_str