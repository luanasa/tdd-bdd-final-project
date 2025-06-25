from service import app
from service.models import Product
from service.common import status
from flask import jsonify, request, abort

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a single Product

    This endpoint will return a Product based on its id
    """
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update a Product

    This endpoint will update a Product based on the body that is posted
    """
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    data = request.get_json()
    if not data:
        abort(status.HTTP_400_BAD_REQUEST, "No data provided for update.")

    product.deserialize(data)
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a Product

    This endpoint will delete a Product based on the id specified in the path
    """
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT

@app.route("/products", methods=["GET"])
def list_products():
    """
    List all Products

    This endpoint will list all Products or filter by query parameters
    """
    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif available:
        available_bool = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_bool)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK

    @app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update a Product"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    data = request.get_json()
    if not data:
        abort(status.HTTP_400_BAD_REQUEST, "No data provided for update.")

    product.deserialize(data)
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK

    @app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a Product"""
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT

    @app.route("/products", methods=["GET"])
def list_products():
    """List all Products"""
    products = Product.all()
    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK

    @app.route("/products", methods=["GET"])
def list_products():
    """List all Products with optional filters"""
    name = request.args.get("name")
    
    if name:
        products = Product.find_by_name(name)
    else:
        products = Product.all()
        
    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK

    from service.models import Product, Category

@app.route("/products", methods=["GET"])
def list_products():
    """List all Products with optional filters"""
    name = request.args.get("name")
    category = request.args.get("category")
    
    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    else:
        products = Product.all()
        
    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK

    @app.route("/products", methods=["GET"])
def list_products():
    """List all Products with optional filters"""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    
    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif available:
        available_bool = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_bool)
    else:
        products = Product.all()
        
    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK