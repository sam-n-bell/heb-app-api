from flask import Blueprint, jsonify

items = Blueprint('items', __name__)

@items.route('/items', methods=['GET'])
def register():
    return jsonify({"message": "items"})