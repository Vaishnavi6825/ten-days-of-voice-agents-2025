# grocery_database.py
from dataclasses import dataclass
from typing import List, Optional, Dict

# --- COMMON INSTRUCTIONS ---
COMMON_INSTRUCTIONS = """
You are a friendly and helpful food & grocery ordering assistant for FreshMart Express.
Be warm, conversational, and make the shopping experience delightful.
Help customers find what they need, suggest items intelligently, and manage their cart efficiently.
Understand natural requests like "I need ingredients for pasta" and add all required items.
"""

# --- PRODUCT DATA STRUCTURE ---
@dataclass
class ProductItem:
    id: str
    name: str
    category: str
    price: float
    brand: str
    size: str
    tags: List[str]
    keywords: List[str]  # For search matching

# --- RECIPE DATA STRUCTURE ---
@dataclass
class RecipeItem:
    name: str
    item_ids: List[str]
    keywords: List[str]

# --- PRODUCT CATALOG ---
PRODUCT_CATALOG = [
    # GROCERIES
    ProductItem(
        id="g001",
        name="Whole Wheat Bread",
        category="groceries",
        price=3.99,
        brand="Nature's Best",
        size="500g",
        tags=["vegan", "whole-grain"],
        keywords=["bread", "whole wheat", "wheat bread", "brown bread"]
    ),
    ProductItem(
        id="g002",
        name="White Bread",
        category="groceries",
        price=2.99,
        brand="Soft Touch",
        size="450g",
        tags=["vegetarian"],
        keywords=["bread", "white bread", "plain bread"]
    ),
    ProductItem(
        id="g003",
        name="Eggs",
        category="groceries",
        price=4.99,
        brand="Farm Fresh",
        size="12 count",
        tags=["protein", "vegetarian"],
        keywords=["eggs", "egg", "dozen eggs"]
    ),
    ProductItem(
        id="g004",
        name="Milk",
        category="groceries",
        price=3.49,
        brand="Dairy Valley",
        size="1 liter",
        tags=["dairy", "vegetarian"],
        keywords=["milk", "dairy", "whole milk"]
    ),
    ProductItem(
        id="g005",
        name="Butter",
        category="groceries",
        price=5.99,
        brand="Golden Spread",
        size="250g",
        tags=["dairy", "vegetarian"],
        keywords=["butter", "dairy butter"]
    ),
    ProductItem(
        id="g006",
        name="Peanut Butter",
        category="groceries",
        price=6.99,
        brand="Nutty Delight",
        size="500g",
        tags=["vegan", "protein"],
        keywords=["peanut butter", "pb", "nut butter"]
    ),
    ProductItem(
        id="g007",
        name="Pasta",
        category="groceries",
        price=2.49,
        brand="Italian Choice",
        size="500g",
        tags=["vegan"],
        keywords=["pasta", "spaghetti", "noodles", "italian"]
    ),
    ProductItem(
        id="g008",
        name="Tomato Sauce",
        category="groceries",
        price=3.99,
        brand="Red Garden",
        size="400ml",
        tags=["vegan", "gluten-free"],
        keywords=["tomato sauce", "pasta sauce", "marinara", "sauce"]
    ),
    ProductItem(
        id="g009",
        name="Olive Oil",
        category="groceries",
        price=8.99,
        brand="Mediterranean Gold",
        size="500ml",
        tags=["vegan", "gluten-free"],
        keywords=["olive oil", "oil", "cooking oil"]
    ),
    ProductItem(
        id="g010",
        name="Rice",
        category="groceries",
        price=7.99,
        brand="Basmati King",
        size="1kg",
        tags=["vegan", "gluten-free"],
        keywords=["rice", "basmati", "grain"]
    ),
    ProductItem(
        id="g011",
        name="Cheese",
        category="groceries",
        price=6.49,
        brand="Cheddar Classic",
        size="300g",
        tags=["dairy", "vegetarian"],
        keywords=["cheese", "cheddar", "dairy"]
    ),
    ProductItem(
        id="g012",
        name="Jam",
        category="groceries",
        price=4.49,
        brand="Berry Best",
        size="350g",
        tags=["vegan", "gluten-free"],
        keywords=["jam", "jelly", "strawberry jam", "fruit spread"]
    ),
    
    # SNACKS
    ProductItem(
        id="s001",
        name="Potato Chips",
        category="snacks",
        price=2.99,
        brand="Crispy Crunch",
        size="150g",
        tags=["vegan"],
        keywords=["chips", "potato chips", "crisps", "snack"]
    ),
    ProductItem(
        id="s002",
        name="Chocolate Bar",
        category="snacks",
        price=1.99,
        brand="Sweet Bliss",
        size="100g",
        tags=["vegetarian"],
        keywords=["chocolate", "candy bar", "sweet"]
    ),
    ProductItem(
        id="s003",
        name="Granola Bars",
        category="snacks",
        price=4.99,
        brand="Energy Boost",
        size="6 pack",
        tags=["vegetarian", "whole-grain"],
        keywords=["granola", "granola bars", "energy bars", "cereal bars"]
    ),
    ProductItem(
        id="s004",
        name="Mixed Nuts",
        category="snacks",
        price=5.99,
        brand="Nutty Mix",
        size="200g",
        tags=["vegan", "protein"],
        keywords=["nuts", "mixed nuts", "almonds", "cashews"]
    ),
    ProductItem(
        id="s005",
        name="Cookies",
        category="snacks",
        price=3.49,
        brand="Baker's Choice",
        size="250g",
        tags=["vegetarian"],
        keywords=["cookies", "biscuits", "chocolate chip"]
    ),
    
    # PREPARED FOOD
    ProductItem(
        id="p001",
        name="Margherita Pizza",
        category="prepared_food",
        price=12.99,
        brand="FreshMart Kitchen",
        size="medium",
        tags=["vegetarian"],
        keywords=["pizza", "margherita", "cheese pizza", "vegetarian pizza"]
    ),
    ProductItem(
        id="p002",
        name="Pepperoni Pizza",
        category="prepared_food",
        price=14.99,
        brand="FreshMart Kitchen",
        size="medium",
        tags=[],
        keywords=["pizza", "pepperoni", "meat pizza"]
    ),
    ProductItem(
        id="p003",
        name="Chicken Sandwich",
        category="prepared_food",
        price=6.99,
        brand="FreshMart Kitchen",
        size="regular",
        tags=[],
        keywords=["sandwich", "chicken sandwich", "chicken", "lunch"]
    ),
    ProductItem(
        id="p004",
        name="Veggie Sandwich",
        category="prepared_food",
        price=5.99,
        brand="FreshMart Kitchen",
        size="regular",
        tags=["vegetarian"],
        keywords=["sandwich", "veggie sandwich", "vegetarian sandwich", "veg"]
    ),
    ProductItem(
        id="p005",
        name="Caesar Salad",
        category="prepared_food",
        price=7.99,
        brand="FreshMart Kitchen",
        size="regular",
        tags=["vegetarian"],
        keywords=["salad", "caesar salad", "healthy", "greens"]
    ),
    ProductItem(
        id="p006",
        name="Burrito Bowl",
        category="prepared_food",
        price=9.99,
        brand="FreshMart Kitchen",
        size="regular",
        tags=[],
        keywords=["burrito", "burrito bowl", "mexican", "rice bowl"]
    ),
]

# --- RECIPE DATABASE ---
RECIPE_CATALOG = [
    RecipeItem(
        name="peanut butter sandwich",
        item_ids=["g001", "g006"],
        keywords=["peanut butter sandwich", "pb sandwich", "pb&j", "peanut butter"]
    ),
    RecipeItem(
        name="pasta",
        item_ids=["g007", "g008", "g009"],
        keywords=["pasta", "spaghetti", "pasta dish", "italian pasta"]
    ),
    RecipeItem(
        name="pasta for two",
        item_ids=["g007", "g008", "g009"],
        keywords=["pasta for two", "pasta for 2", "pasta two people"]
    ),
    RecipeItem(
        name="breakfast",
        item_ids=["g002", "g003", "g004", "g005"],
        keywords=["breakfast", "morning meal", "basic breakfast"]
    ),
    RecipeItem(
        name="cheese sandwich",
        item_ids=["g002", "g011", "g005"],
        keywords=["cheese sandwich", "grilled cheese"]
    ),
    RecipeItem(
        name="toast with jam",
        item_ids=["g001", "g012", "g005"],
        keywords=["toast", "jam toast", "bread and jam"]
    ),
]

# --- SEARCH FUNCTIONS ---
def search_products(query: str) -> List[ProductItem]:
    """
    Search for products by name, brand, tags, or keywords.
    Returns a list of matching products.
    """
    query_lower = query.lower()
    results = []
    
    for product in PRODUCT_CATALOG:
        # Check name, brand, category, tags, and keywords
        if (query_lower in product.name.lower() or
            query_lower in product.brand.lower() or
            query_lower in product.category.lower() or
            any(query_lower in tag.lower() for tag in product.tags) or
            any(query_lower in keyword.lower() for keyword in product.keywords)):
            results.append(product)
    
    return results

def find_product_by_id(product_id: str) -> Optional[ProductItem]:
    """Find a product by its ID."""
    for product in PRODUCT_CATALOG:
        if product.id == product_id:
            return product
    return None

def find_recipe(recipe_name: str) -> Optional[RecipeItem]:
    """
    Find a recipe by name or keywords.
    Returns the recipe if found, else None.
    """
    recipe_name_lower = recipe_name.lower().strip()
    
    for recipe in RECIPE_CATALOG:
        # Check exact name match
        if recipe_name_lower == recipe.name.lower():
            return recipe
        
        # Check keywords
        for keyword in recipe.keywords:
            if recipe_name_lower in keyword.lower() or keyword.lower() in recipe_name_lower:
                return recipe
    
    return None

def get_all_products_by_category(category: str) -> List[ProductItem]:
    """Get all products in a specific category."""
    return [p for p in PRODUCT_CATALOG if p.category.lower() == category.lower()]

def get_products_by_tag(tag: str) -> List[ProductItem]:
    """Get all products with a specific tag."""
    return [p for p in PRODUCT_CATALOG if tag.lower() in [t.lower() for t in p.tags]]

# --- HELPER CLASS ---
class GroceryDB:
    """Helper class for grocery database operations."""
    
    @staticmethod
    def search(query: str) -> List[ProductItem]:
        return search_products(query)
    
    @staticmethod
    def get_product(product_id: str) -> Optional[ProductItem]:
        return find_product_by_id(product_id)
    
    @staticmethod
    def get_recipe(recipe_name: str) -> Optional[RecipeItem]:
        return find_recipe(recipe_name)
    
    @staticmethod
    def get_all_products() -> List[ProductItem]:
        return PRODUCT_CATALOG
    
    @staticmethod
    def get_all_recipes() -> List[RecipeItem]:
        return RECIPE_CATALOG
    
    @staticmethod
    def get_category(category: str) -> List[ProductItem]:
        return get_all_products_by_category(category)
    
    @staticmethod
    def get_by_tag(tag: str) -> List[ProductItem]:
        return get_products_by_tag(tag)