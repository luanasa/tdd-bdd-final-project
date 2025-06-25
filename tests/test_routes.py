from service import app
from service.models import Product, db
from service.common import status
from tests.factories import ProductFactory
import json

BASE_URL = "/products"

class TestProductRoutes:
    """Test Cases for Product Routes"""

    @classmethod
    def setup_class(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        with app.app_context():
            db.drop_all()
            db.create_all()

    def setup_method(self, method):
        """Run before each test"""
        with app.app_context():
            db.session.query(Product).delete()
            db.session.commit()
        self.client = app.test_client()

    def _create_products(self, count):
        """Helper method to create products"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(
                BASE_URL,
                json=test_product.serialize(),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            products.append(response.get_json())
        return products

    def test_get_product(self):
        """It should Get a single Product"""
        # Create a product first
        test_product = self._create_products(1)[0]
        
        # Now get it back
        response = self.client.get(f"{BASE_URL}/{test_product['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product["name"])
        self.assertEqual(data["description"], test_product["description"])
        self.assertEqual(float(data["price"]), float(test_product["price"]))
        self.assertEqual(data["available"], test_product["available"])
        self.assertEqual(data["category"], test_product["category"])

    def test_get_product_not_found(self):
        """It should not Get a Product that doesn't exist"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """It should Update an existing Product"""
        # Create a product first
        test_product = self._create_products(1)[0]
        
        # Update the product
        test_product["description"] = "Updated description"
        response = self.client.put(
            f"{BASE_URL}/{test_product['id']}",
            json=test_product,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["description"], "Updated description")

    def test_delete_product(self):
        """It should Delete a Product"""
        # Create a product first
        test_product = self._create_products(1)[0]
        
        # Delete the product
        response = self.client.delete(f"{BASE_URL}/{test_product['id']}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify it's deleted
        response = self.client.get(f"{BASE_URL}/{test_product['id']}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_products(self):
        """It should List all Products"""
        # Create 5 products
        self._create_products(5)
        
        # List all products
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_list_products_by_name(self):
        """It should List Products by name"""
        # Create products with different names
        self._create_products(3)
        test_product = ProductFactory(name="Special Product")
        response = self.client.post(
            BASE_URL,
            json=test_product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # List products by name
        response = self.client.get(
            BASE_URL,
            query_string={"name": "Special Product"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Special Product")

    def test_list_products_by_category(self):
        """It should List Products by category"""
        # Create products with different categories
        self._create_products(3)
        test_product = ProductFactory(category="FOOD")
        response = self.client.post(
            BASE_URL,
            json=test_product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # List products by category
        response = self.client.get(
            BASE_URL,
            query_string={"category": "FOOD"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "FOOD")

    def test_list_products_by_availability(self):
        """It should List Products by availability"""
        # Create products with different availability
        self._create_products(3)
        test_product = ProductFactory(available=False)
        response = self.client.post(
            BASE_URL,
            json=test_product.serialize(),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # List products by availability
        response = self.client.get(
            BASE_URL,
            query_string={"available": "false"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["available"], False)

        def test_update_product(self):
    """It should Update an existing Product"""
    # Create a product first
    test_product = self._create_products(1)[0]
    
    # Update the product
    test_product["description"] = "Updated description"
    response = self.client.put(
        f"{BASE_URL}/{test_product['id']}",
        json=test_product,
        content_type="application/json"
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(data["description"], "Updated description")

    def test_delete_product(self):
    """It should Delete a Product"""
    test_product = self._create_products(1)[0]
    
    response = self.client.delete(f"{BASE_URL}/{test_product['id']}")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # Verify it's deleted
    response = self.client.get(f"{BASE_URL}/{test_product['id']}")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_products(self):
    """It should List all Products"""
    self._create_products(5)
    
    response = self.client.get(BASE_URL)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(len(data), 5)

    from urllib.parse import quote_plus

def test_list_products_by_name(self):
    """It should List Products by name"""
    self._create_products(3)
    test_product = ProductFactory(name="Special Product")
    response = self.client.post(
        BASE_URL,
        json=test_product.serialize(),
        content_type="application/json"
    )
    
    response = self.client.get(
        BASE_URL,
        query_string={"name": "Special Product"}
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(len(data), 1)
    self.assertEqual(data[0]["name"], "Special Product")

    def test_list_products_by_category(self):
    """It should List Products by category"""
    self._create_products(3)
    test_product = ProductFactory(category="FOOD")
    response = self.client.post(
        BASE_URL,
        json=test_product.serialize(),
        content_type="application/json"
    )
    
    response = self.client.get(
        BASE_URL,
        query_string={"category": "FOOD"}
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(len(data), 1)
    self.assertEqual(data[0]["category"], "FOOD")

    def test_list_products_by_availability(self):
    """It should List Products by availability"""
    self._create_products(3)
    test_product = ProductFactory(available=False)
    response = self.client.post(
        BASE_URL,
        json=test_product.serialize(),
        content_type="application/json"
    )
    
    response = self.client.get(
        BASE_URL,
        query_string={"available": "false"}
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(len(data), 1)
    self.assertEqual(data[0]["available"], False)