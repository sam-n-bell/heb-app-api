from hebapp.products.models import ProductView, ProductViewSchema

def serialize_many(views):
    view_schema = ProductViewSchema()
    return view_schema.dump(views, many=True)

def serialize_one(view):
    view_schema = ProductViewSchema()
    return view_schema.dump(view, many=False)