import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal, FuzzyText
from service.models import Product, Category
from datetime import datetime, timedelta

class ProductFactory(factory.Factory):
    """Creates realistic fake products for comprehensive testing"""
    
    class Meta:
        model = Product
    
    # ID generation with larger starting number to avoid conflicts
    id = factory.Sequence(lambda n: n + 1000)
    
    # Enhanced name generation with brand+product combinations
    name = factory.LazyAttribute(
        lambda x: f"{FuzzyChoice(['Nike', 'Adidas', 'Sony', 'Apple', 'Samsung', 'Dell']).fuzz()} "
                 f"{FuzzyChoice(['Pro', 'Max', 'Lite', 'Air', 'X']).fuzz()} "
                 f"{FuzzyChoice(['T-Shirt', 'Jeans', 'Phone', 'Laptop', 'Watch', 'Shoes']).fuzz()}"
    )
    
    # More structured descriptions
    description = factory.Faker(
        'paragraph', 
        nb_sentences=3,
        ext_word_list=['high-quality', 'durable', 'eco-friendly', 'premium', 'ergonomic']
    )
    
    # Realistic price distribution with common price endings
    price = FuzzyDecimal(
        1.0, 
        999.99,
        precision=2
    ).add_choice(
        factory.Iterator([9.99, 19.99, 29.99, 49.99, 99.99])  # Common price points
    )
    
    # Availability with business logic (new products more likely available)
    available = factory.LazyAttribute(
        lambda x: datetime.now() - x.manufacture_date < timedelta(days=365)
    )
    
    # Category with weighted distribution
    category = FuzzyChoice(
        choices=[
            (Category.CLOTHS, 30),
            (Category.FOOD, 20),
            (Category.HOUSEWARES, 20),
            (Category.AUTOMOTIVE, 15),
            (Category.TOOLS, 10),
            (Category.UNKNOWN, 5)
        ]
    )
    
    # Additional realistic product attributes
    sku = factory.LazyAttribute(
        lambda x: f"SKU-{FuzzyText(length=6, chars='0123456789').fuzz()}"
    )
    
    manufacture_date = factory.Faker(
        'date_between', 
        start_date='-5y', 
        end_date='today'
    )
    
    weight = FuzzyDecimal(0.1, 20.0, 1)
    
    rating = FuzzyDecimal(1.0, 5.0, 1)
    
    @factory.post_generation
    def promotions(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            # Add passed promotions
            for promotion in extracted:
                self.promotions.add(promotion)