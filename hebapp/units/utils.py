from hebapp.units.models import UnitSchema

def serialize_many(units):
    unit_schema = UnitSchema()
    return unit_schema.dump(units, many=True)

def serialize_one(unit):
    unit_schema = UnitSchema()
    return unit_schema.dump(unit, many=False)