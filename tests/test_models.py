"""
Test cases for Product Model
"""
import logging
import pytest
from werkzeug.exceptions import NotFound
from service.models import Product, db, DataValidationError
from tests.factories import ProductFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def app():
    """Setup the test app"""
    from service import app
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def database(app):
    """Clean the database between tests"""
    db.session.query(Product).delete()
    db.session.commit()

class TestProductModel:
    """Test suite for the Product model"""

    def test_create_product(self, database):
        """It should create a Product and assert its properties"""
        product = ProductFactory()
        logger.info("Test Product: %s", product)
        assert product is not None
        assert product.id is None
        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.available, bool)
        assert product.category in [
            Category.UNKNOWN,
            Category.CLOTHS,
            Category.FOOD,
            Category.HOUSEWARES,
            Category.AUTOMOTIVE,
            Category.TOOLS
        ]

    def test_add_product(self, database):
        """It should add a Product to the database"""
        products = Product.all()
        assert len(products) == 0

        product = ProductFactory()
        product.create()
        
        assert product.id is not None
        assert Product.all().count() == 1

    def test_read_product(self, database):
        """It should read a Product from the database"""
        # Create test data
        original_product = ProductFactory()
        original_product.create()
        
        # Test retrieval
        found_product = Product.find(original_product.id)
        assert found_product is not None
        assert found_product.id == original_product.id
        assert found_product.name == original_product.name
        assert found_product.description == original_product.description
        assert float(found_product.price) == float(original_product.price)
        assert found_product.available == original_product.available
        assert found_product.category == original_product.category

    def test_update_product(self, database):
        """It should update a Product in the database"""
        # Create test data
        product = ProductFactory()
        product.create()
        original_id = product.id
        
        # Update product
        new_description = "Updated description"
        product.description = new_description
        product.update()
        
        # Verify changes
        assert product.id == original_id
        assert product.description == new_description
        assert Product.all().count() == 1
        
        # Verify in database
        updated_product = Product.find(original_id)
        assert updated_product.description == new_description

    def test_delete_product(self, database):
        """It should delete a Product from the database"""
        product = ProductFactory()
        product.create()
        assert Product.all().count() == 1
        
        product.delete()
        assert Product.all().count() == 0

    def test_list_all_products(self, database):
        """It should list all Products in the database"""
        assert Product.all().count() == 0
        
        # Create test data
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        
        assert Product.all().count() == 5

    def test_find_by_name(self, database):
        """It should find Products by name"""
        # Create test data with known names
        target_name = "Special Product"
        ProductFactory(name=target_name).create()
        ProductFactory(name=target_name).create()
        ProductFactory.create_batch(3)  # Other products
        
        # Test find by name
        found_products = Product.find_by_name(target_name)
        assert found_products.count() == 2
        for product in found_products:
            assert product.name == target_name

    def test_find_by_availability(self, database):
        """It should find Products by availability"""
        # Create test data with known availability
        ProductFactory(available=True).create()
        ProductFactory(available=True).create()
        ProductFactory(available=False).create()
        
        # Test find by availability
        available_products = Product.find_by_availability(True)
        assert available_products.count() == 2
        
        unavailable_products = Product.find_by_availability(False)
        assert unavailable_products.count() == 1

    def test_find_by_category(self, database):
        """It should find Products by category"""
        # Create test data with known categories
        target_category = Category.CLOTHS
        ProductFactory(category=target_category).create()
        ProductFactory(category=target_category).create()
        ProductFactory.create_batch(3)  # Other categories
        
        # Test find by category
        found_products = Product.find_by_category(target_category)
        assert found_products.count() == 2
        for product in found_products:
            assert product.category == target_category

    def test_serialize_product(self, database):
        """It should serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        
        assert data["id"] == product.id
        assert data["name"] == product.name
        assert data["description"] == product.description
        assert float(data["price"]) == float(product.price)
        assert data["available"] == product.available
        assert data["category"] == product.category.name

    def test_deserialize_product(self, database):
        """It should deserialize a Product"""
        original_product = ProductFactory()
        data = original_product.serialize()
        
        new_product = Product()
        new_product.deserialize(data)
        
        assert new_product.name == original_product.name
        assert new_product.description == original_product.description
        assert float(new_product.price) == float(original_product.price)
        assert new_product.available == original_product.available
        assert new_product.category == original_product.category

    def test_deserialize_invalid_data(self, database):
        """It should handle deserialization errors"""
        invalid_data = [
            {"name": 123},  # Wrong type
            {"name": "Test", "price": "not-a-number"},  # Invalid price
            {},  # Missing data
            {"name": "Test", "category": "INVALID_CATEGORY"}  # Bad category
        ]
        
        product = Product()
        for data in invalid_data:
            with pytest.raises(DataValidationError):
                product.deserialize(data)

    def test_find_missing_product(self, database):
        """It should handle missing product lookups"""
        assert Product.find(999999) is None

    def test_update_missing_product(self, database):
        """It should handle updating non-existent products"""
        product = ProductFactory()
        product.id = 999999
        with pytest.raises(NotFound):
            product.update()

    def test_delete_missing_product(self, database):
        """It should handle deleting non-existent products"""
        product = ProductFactory()
        product.id = 999999
        with pytest.raises(NotFound):
            product.delete()