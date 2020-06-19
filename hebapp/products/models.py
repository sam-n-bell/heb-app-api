from hebapp import db, ma
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow import Schema, fields
from hebapp.departments.models import Department
from marshmallow import Schema
from citext import CIText


class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(CIText(), unique=True, nullable=False)
    last_sold = db.Column(db.Date, nullable=True)
    shelf_life = db.Column(db.Integer, nullable=True)
    sell_price = db.Column(db.Float, nullable=False)
    cost_expense = db.Column(db.Float, nullable=False)
    qty_sold_in = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable = False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable = False)

    def __repr__(self):
        return f'Product({self.product_id}, {self.description}, {self.last_sold}, {self.shelf_life}, {self.sell_price})'

class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = (
            "product_id",
            "description",
            "last_sold",
            "shelf_life",
            "sell_price",
            "cost_expense",
            "qty_sold_in",
            "department_id",
            "unit_id"
        )

# used for marshmallow validation        
class ProductModelSchema(ma.Schema):
    description = fields.Str(required=True, validate=Length(min=2, max=100))
    last_sold = fields.Date()
    shelf_life = fields.Integer(required=False, validate=Range(min=1))
    sell_price = fields.Float(required=True, validate=Range(min=0))
    cost_expense = fields.Float(required=True, validate=Range(min=0))
    qty_sold_in = fields.Integer(required=False, validate=Range(min=1))
    department_id = fields.Integer(required=True)
    unit_id = fields.Integer(required=True)


# this is actually a VIEW table in the database. Don't try writing to it!
class ProductView(db.Model):
    __tablename__ = 'products_view'
    product_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(CIText(), unique=True, nullable=False)
    last_sold = db.Column(db.Date, nullable=True)
    shelf_life = db.Column(db.Integer, nullable=True)
    sell_price = db.Column(db.Float, nullable=False)
    cost_expense = db.Column(db.Float, nullable=False)
    qty_sold_in = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(50), nullable = False)
    unit = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'ProductView({self.product_id}, {self.description}, {self.last_sold}, {self.shelf_life}, {self.sell_price}, {self.cost_expense}, {self.qty_sold_in}, {self.department}, {self.unit})'

class ProductViewSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = (
            "product_id",
            "description",
            "last_sold",
            "shelf_life",
            "sell_price",
            "cost_expense",
            "qty_sold_in",
            "department",
            "unit"
        )