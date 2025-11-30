# Product catalog following ACP (Agentic Commerce Protocol) structure

PRODUCTS = [
    # Coffee Mugs
    {
        "id": "mug-001",
        "name": "Stoneware Coffee Mug - Classic White",
        "description": "Premium ceramic stoneware mug with elegant minimalist design",
        "price": 800,
        "currency": "INR",
        "category": "mug",
        "color": "white",
        "stock": 50,
    },
    {
        "id": "mug-002",
        "name": "Ceramic Coffee Mug - Blue Marble",
        "description": "Beautiful marble pattern ceramic mug perfect for your morning coffee",
        "price": 950,
        "currency": "INR",
        "category": "mug",
        "color": "blue",
        "stock": 35,
    },
    {
        "id": "mug-003",
        "name": "Glass Coffee Mug - Transparent",
        "description": "Double-walled borosilicate glass mug, keeps beverages hot longer",
        "price": 1200,
        "currency": "INR",
        "category": "mug",
        "color": "transparent",
        "stock": 40,
    },
    {
        "id": "mug-004",
        "name": "Ceramic Coffee Mug - Black Minimalist",
        "description": "Sleek black ceramic mug with modern aesthetic",
        "price": 750,
        "currency": "INR",
        "category": "mug",
        "color": "black",
        "stock": 60,
    },
    
    # T-Shirts
    {
        "id": "tshirt-001",
        "name": "Cotton T-Shirt - Plain White",
        "description": "100% organic cotton comfortable t-shirt for everyday wear",
        "price": 499,
        "currency": "INR",
        "category": "t-shirt",
        "color": "white",
        "size": "S, M, L, XL, XXL",
        "stock": 100,
    },
    {
        "id": "tshirt-002",
        "name": "Graphic T-Shirt - Navy Blue",
        "description": "Trendy graphic t-shirt with modern design print",
        "price": 699,
        "currency": "INR",
        "category": "t-shirt",
        "color": "navy blue",
        "size": "S, M, L, XL",
        "stock": 75,
    },
    {
        "id": "tshirt-003",
        "name": "Premium T-Shirt - Black",
        "description": "High-quality premium cotton t-shirt with superior comfort",
        "price": 899,
        "currency": "INR",
        "category": "t-shirt",
        "color": "black",
        "size": "XS, S, M, L, XL, XXL",
        "stock": 85,
    },
    {
        "id": "tshirt-004",
        "name": "Sports T-Shirt - Red",
        "description": "Moisture-wicking sports t-shirt for athletic activities",
        "price": 1099,
        "currency": "INR",
        "category": "t-shirt",
        "color": "red",
        "size": "M, L, XL",
        "stock": 45,
    },
    
    # Hoodies
    {
        "id": "hoodie-001",
        "name": "Cotton Hoodie - Black Classic",
        "description": "Comfortable black hoodie perfect for casual wear",
        "price": 1999,
        "currency": "INR",
        "category": "hoodie",
        "color": "black",
        "size": "S, M, L, XL, XXL",
        "stock": 40,
    },
    {
        "id": "hoodie-002",
        "name": "Premium Fleece Hoodie - Navy Blue",
        "description": "Soft fleece lining hoodie with kangaroo pocket, ultra-comfortable",
        "price": 2499,
        "currency": "INR",
        "category": "hoodie",
        "color": "navy blue",
        "size": "M, L, XL",
        "stock": 35,
    },
    {
        "id": "hoodie-003",
        "name": "Athletic Hoodie - Grey",
        "description": "Performance athletic hoodie with breathable fabric",
        "price": 2299,
        "currency": "INR",
        "category": "hoodie",
        "color": "grey",
        "size": "S, M, L, XL",
        "stock": 50,
    },
    {
        "id": "hoodie-004",
        "name": "Oversized Hoodie - White",
        "description": "Trendy oversized hoodie for relaxed comfort",
        "price": 2199,
        "currency": "INR",
        "category": "hoodie",
        "color": "white",
        "size": "M, L, XL, XXL",
        "stock": 45,
    },
    {
        "id": "hoodie-005",
        "name": "Premium Hoodie - Charcoal",
        "description": "High-end charcoal hoodie with premium finish",
        "price": 2799,
        "currency": "INR",
        "category": "hoodie",
        "color": "charcoal",
        "size": "S, M, L, XL",
        "stock": 30,
    },
    
    # Accessories
    {
        "id": "cap-001",
        "name": "Baseball Cap - Black",
        "description": "Classic black baseball cap with adjustable strap",
        "price": 599,
        "currency": "INR",
        "category": "cap",
        "color": "black",
        "stock": 100,
    },
    {
        "id": "cap-002",
        "name": "Sports Cap - White",
        "description": "Breathable sports cap with moisture-wicking band",
        "price": 799,
        "currency": "INR",
        "category": "cap",
        "color": "white",
        "stock": 80,
    },
]

# Example of how to use filtering
def get_products_by_category(category: str) -> list:
    """Get all products in a specific category"""
    return [p for p in PRODUCTS if p.get("category", "").lower() == category.lower()]

def get_products_under_price(max_price: int) -> list:
    """Get all products under a specific price"""
    return [p for p in PRODUCTS if p.get("price", 0) <= max_price]

def get_product_by_id(product_id: str) -> dict:
    """Get a specific product by ID"""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None