from hebapp import db, ma
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow import Schema, fields
from citext import CIText

class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(CIText(), unique=True, nullable=False)
    products = db.relationship('Product', backref="department", lazy=True)

    def __repr__(self):
        return f'Department({self.department_id}, {self.name})'

class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = (
            "department_id",
            "name"
        )