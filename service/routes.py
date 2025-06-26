from flask import request, jsonify, abort
from service import app
from service.models import Product, Category, DataValidationError
from service.common import status
from urllib.parse import quote_plus

@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based on the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    
    product = Product()
    try:
        product.deserialize(request.get_json())
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))
    
    product.create()
    app.logger.info("Product with ID [%s] created.", product.id)
    return jsonify(product.serialize()), status.HTTP_201_CREATED

@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on its id
    """
    app.logger.info("Request to get product with id: %s", product_id)
    
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    
    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product
    This endpoint will update a Product based on the body that is posted
    """
    app.logger.info("Request to update product with id: %s", product_id)
    check_content_type("application/json")
    
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    
    try:
        product.deserialize(request.get_json())
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))
    
    product.update()
    app.logger.info("Product with ID [%s] updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product
    This endpoint will delete a Product based on the id specified in the path
    """
    app.logger.info("Request to delete product with id: %s", product_id)
    
    product = Product.find(product_id)
    if product:
        product.delete()
    
    app.logger.info("Product with ID [%s] delete complete.", product_id)
    return "", status.HTTP_204_NO_CONTENT

@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products with optional filtering"""
    app.logger.info("Request to list products")
    
    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    
    if name:
        app.logger.info("Filtering by name: %s", name)
        products = Product.find_by_name(name)
    elif category:
        app.logger.info("Filtering by category: %s", category)
        try:
            # Convert string category to enum value
            category_enum = Category[category.upper()]
            products = Product.find_by_category(category_enum)
        except KeyError:
            abort(status.HTTP_400_BAD_REQUEST, f"Invalid category: {category}")
    elif available is not None:
        app.logger.info("Filtering by availability: %s", available)
        available_bool = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_bool)
    else:
        app.logger.info("Returning all products")
        products = Product.all()
    
    results = [product.serialize() for product in products]
    app.logger.info("[%s] Products returned", len(results))
    return jsonify(results), status.HTTP_200_OK

def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be {}".format(content_type))
    
    if request.headers["Content-Type"] != content_type:
        app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be {}".format(content_type))