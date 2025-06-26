class Product(db.Model):
    # ... (existing model definition remains the same)

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available,
            "category": self.category if isinstance(self.category, str) else self.category.name
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary
        
        Args:
            data (dict): A dictionary containing the Product data
        """
        try:
            self.name = data["name"]
            self.description = data.get("description")
            self.price = float(data["price"])
            self.available = data.get("available", True)
            
            # Handle category which can be string or enum
            category = data.get("category")
            if isinstance(category, str):
                try:
                    self.category = Category[category.upper()].name
                except KeyError:
                    raise DataValidationError(f"Invalid category: {category}")
            else:
                self.category = Category(category).name
                
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " + error.args[0])
        except (TypeError, ValueError) as error:
            raise DataValidationError("Invalid product: " + str(error))

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Starting database")
        db.init_app(app)
        with app.app_context():
            db.create_all()

    @classmethod
    def all(cls):
        """Returns all Products"""
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        """Finds a Product by its ID"""
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name).all()

    @classmethod
    def find_by_category(cls, category):
        """Returns all Products in the given category"""
        logger.info("Processing category query for %s ...", category.name)
        return cls.query.filter(cls.category == category.name).all()

    @classmethod
    def find_by_availability(cls, available=True):
        """Returns all Products by availability"""
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available).all()

    def create(self):
        """Creates a Product to the database"""
        logger.info("Creating %s", self.name)
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a Product to the database"""
        logger.info("Updating %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Product from the database"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()