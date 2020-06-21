from hebapp.departments.models import DepartmentSchema

def serialize_many(departments):
    department_schema = DepartmentSchema()
    return department_schema.dump(departments, many=True)

def serialize_one(department):
    department_schema = DepartmentSchema()
    return department_schema.dump(departments, many=False)