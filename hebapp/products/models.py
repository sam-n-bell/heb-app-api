from hebapp import db, ma
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow import Schema, fields
from hebapp.departments.models import Department

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=True, nullable=False)
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