from flask import request, jsonify, abort
from service import app
from service.models import Product
from service.common import status

@app.route("/products", methods=["POST"])
def create_products():
    """Create a new Product"""
    data = request.get_json()
    product = Product()
    product.deserialize(data)
    product.create()
    
    return jsonify(product.serialize()), status.HTTP_201_CREATED

@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Get a single Product"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Update a Product"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    
    data = request.get_json()
    product.deserialize(data)
    product.update()
    
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Delete a Product"""
    product = Product.find(product_id)
    if product:
        product.delete()
    
    return "", status.HTTP_204_NO_CONTENT

@app.route("/products", methods=["GET"])
def list_products():
    """List all products with optional filtering"""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    
    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif available:
        available_bool = available.lower() == "true"
        products = Product.find_by_availability(available_bool)
    else:
        products = Product.all()
    
    return jsonify([product.serialize() for product in products]), status.HTTP_200_OK