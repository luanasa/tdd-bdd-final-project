from service.models import Product, db
from tests.factories import ProductFactory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestProductModel:
    """Test suite for the Product model"""

    def test_create_product(self):
        """It should create a Product and assert its properties"""
        product = ProductFactory()
        logger.info("Test Product: %s", product)
        assert product is not None
        assert product.id is None
        assert product.name is not None
        assert product.description is not None
        assert product.price is not None
        assert product.available is not None
        assert product.category is not None

    def test_add_product(self):
        """It should add a Product to the database"""
        products = Product.all()
        product_count = len(products)
        assert product_count == 0

        product = ProductFactory()
        product.create()
        
        # Assert that it was assigned an id and shows up in the database
        assert product.id is not None
        products = Product.all()
        assert len(products) == product_count + 1

    def test_read_product(self):
        """It should read a Product from the database"""
        product = ProductFactory()
        logger.info("Test Product: %s", product)
        product.id = None
        product.create()
        assert product.id is not None
        
        # Fetch it back
        found_product = Product.find(product.id)
        assert found_product.id == product.id
        assert found_product.name == product.name
        assert found_product.description == product.description
        assert float(found_product.price) == float(product.price)
        assert found_product.available == product.available
        assert found_product.category == product.category

    def test_update_product(self):
        """It should update a Product in the database"""
        product = ProductFactory()
        logger.info("Test Product: %s", product)
        product.id = None
        product.create()
        logger.info("Product created: %s", product)
        assert product.id is not None
        
        # Update it
        original_id = product.id
        product.description = "New description"
        product.update()
        
        assert product.id == original_id
        assert product.description == "New description"
        
        # Fetch it back and check
        products = Product.all()
        assert len(products) == 1
        assert products[0].id == original_id
        assert products[0].description == "New description"

    def test_delete_product(self):
        """It should delete a Product from the database"""
        product = ProductFactory()
        product.create()
        products = Product.all()
        assert len(products) == 1
        
        # Delete it
        product.delete()
        products = Product.all()
        assert len(products) == 0

    def test_list_all_products(self):
        """It should list all Products in the database"""
        products = Product.all()
        assert len(products) == 0
        
        # Create 5 products
        for _ in range(5):
            product = ProductFactory()
            product.create()
        
        products = Product.all()
        assert len(products) == 5

    def test_find_by_name(self):
        """It should find Products by name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = Product.find_by_name(name)
        assert len(found) == count
        for product in found:
            assert product.name == name

    def test_find_by_availability(self):
        """It should find Products by availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        
        available = products[0].available
        count = len([product for product in products if product.available == available])
        found = Product.find_by_availability(available)
        assert len(found) == count
        for product in found:
            assert product.available == available

    def test_find_by_category(self):
        """It should find Products by category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        
        category = products[0].category
        count = len([product for product in products if product.category == category])
        found = Product.find_by_category(category)
        assert len(found) == count
        for product in found:
            assert product.category == category