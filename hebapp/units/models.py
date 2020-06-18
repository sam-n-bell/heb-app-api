from hebapp import db, ma
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow import Schema, fields

class Unit(db.Model):
    __tablename__ = 'units'
    unit_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Product', backref="unit", lazy=True)

    def __repr__(self):
        return f'Unit({self.unit_id}, {self.name})'

class UnitSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = (
            "unit_id",
            "name"
        )