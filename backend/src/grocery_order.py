# grocery_order.py
from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# --- CART ITEM MODEL ---
class CartItem(BaseModel):
    """Represents an item in the shopping cart."""
    item_id: str
    name: str
    quantity: int
    price: float
    brand: str
    size: str
    category: str
    
    def get_total(self) -> float:
        """Calculate total price for this item."""
        return self.price * self.quantity

# --- ORDER MODEL ---
class OrderItem(BaseModel):
    """Base class for orders."""
    order_id: str = Field(default_factory=lambda: f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}")

class OrderData(OrderItem):
    """Complete order information."""
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    customer_name: str
    delivery_address: str
    phone: str = "Not Provided"
    items: List[Dict]
    total_amount: float
    status: str = "placed"
    special_instructions: str = ""

# --- CART STATE MANAGEMENT ---
class CartState:
    """Manages the shopping cart during the session."""
    
    def __init__(self):
        self.items: Dict[str, CartItem] = {}
    
    def add_item(self, item_id: str, name: str, quantity: int, price: float, 
                 brand: str, size: str, category: str) -> CartItem:
        """
        Add an item to the cart or update quantity if it already exists.
        Returns the cart item.
        """
        if item_id in self.items:
            # Update quantity if item already exists
            self.items[item_id].quantity += quantity
        else:
            # Add new item
            self.items[item_id] = CartItem(
                item_id=item_id,
                name=name,
                quantity=quantity,
                price=price,
                brand=brand,
                size=size,
                category=category
            )
        
        return self.items[item_id]
    
    def remove_item(self, item_id: str) -> Optional[CartItem]:
        """Remove an item from the cart."""
        if item_id in self.items:
            return self.items.pop(item_id)
        return None
    
    def update_quantity(self, item_id: str, quantity: int) -> bool:
        """
        Update the quantity of an item in the cart.
        If quantity is 0 or less, the item is removed.
        Returns True if successful, False otherwise.
        """
        if item_id not in self.items:
            return False
        
        if quantity <= 0:
            self.remove_item(item_id)
            return True
        
        self.items[item_id].quantity = quantity
        return True
    
    def get_item(self, item_id: str) -> Optional[CartItem]:
        """Get a specific item from the cart."""
        return self.items.get(item_id)
    
    def get_all_items(self) -> List[CartItem]:
        """Get all items in the cart."""
        return list(self.items.values())
    
    def get_total(self) -> float:
        """Calculate the total price of all items in the cart."""
        return sum(item.get_total() for item in self.items.values())
    
    def get_item_count(self) -> int:
        """Get the total number of items in the cart."""
        return sum(item.quantity for item in self.items.values())
    
    def is_empty(self) -> bool:
        """Check if the cart is empty."""
        return len(self.items) == 0
    
    def clear(self) -> None:
        """Clear all items from the cart."""
        self.items.clear()
    
    def get_summary(self) -> str:
        """
        Get a text summary of the cart contents.
        Returns a formatted string with all items and total.
        """
        if self.is_empty():
            return "Your cart is empty."
        
        summary_lines = []
        summary_lines.append("🛒 Your Cart:")
        summary_lines.append("-" * 50)
        
        for item in self.items.values():
            item_total = item.get_total()
            summary_lines.append(
                f"{item.quantity}x {item.name} ({item.brand}, {item.size}) - ${item_total:.2f}"
            )
        
        summary_lines.append("-" * 50)
        summary_lines.append(f"Total: ${self.get_total():.2f}")
        summary_lines.append(f"Items: {self.get_item_count()}")
        
        return "\n".join(summary_lines)
    
    def get_items_by_category(self, category: str) -> List[CartItem]:
        """Get all items in a specific category."""
        return [item for item in self.items.values() if item.category.lower() == category.lower()]
    
    def has_item(self, item_id: str) -> bool:
        """Check if an item is in the cart."""
        return item_id in self.items

# --- ORDER STATE MANAGEMENT ---
class OrderState:
    """Manages orders placed during the session."""
    
    def __init__(self):
        self.orders: Dict[str, OrderData] = {}
    
    def create_order(self, customer_name: str, delivery_address: str, 
                    cart_items: List[CartItem], phone: str = "Not Provided",
                    special_instructions: str = "") -> OrderData:
        """
        Create a new order from cart items.
        Returns the created order.
        """
        # Convert cart items to dict format
        items_data = []
        for item in cart_items:
            items_data.append({
                "item_id": item.item_id,
                "name": item.name,
                "brand": item.brand,
                "size": item.size,
                "quantity": item.quantity,
                "price": item.price,
                "total_price": item.get_total(),
                "category": item.category
            })
        
        # Calculate total
        total_amount = sum(item.get_total() for item in cart_items)
        
        # Create order
        order = OrderData(
            customer_name=customer_name,
            delivery_address=delivery_address,
            phone=phone,
            items=items_data,
            total_amount=total_amount,
            special_instructions=special_instructions
        )
        
        self.orders[order.order_id] = order
        return order
    
    def get_order(self, order_id: str) -> Optional[OrderData]:
        """Get an order by ID."""
        return self.orders.get(order_id)
    
    def get_all_orders(self) -> List[OrderData]:
        """Get all orders."""
        return list(self.orders.values())
    
    def get_latest_order(self) -> Optional[OrderData]:
        """Get the most recent order."""
        if not self.orders:
            return None
        return list(self.orders.values())[-1]
    
    def clear(self) -> None:
        """Clear all orders."""
        self.orders.clear()

# --- ORDER SUMMARY HELPER ---
def format_order_summary(order: OrderData) -> str:
    """
    Format an order into a readable summary.
    """
    lines = []
    lines.append(f"📦 Order {order.order_id}")
    lines.append(f"Date: {order.timestamp}")
    lines.append(f"Customer: {order.customer_name}")
    lines.append(f"Delivery Address: {order.delivery_address}")
    if order.phone != "Not Provided":
        lines.append(f"Phone: {order.phone}")
    lines.append("-" * 50)
    lines.append("Items:")
    
    for item in order.items:
        lines.append(
            f"  {item['quantity']}x {item['name']} ({item['brand']}, {item['size']}) - ${item['total_price']:.2f}"
        )
    
    lines.append("-" * 50)
    lines.append(f"Total: ${order.total_amount:.2f}")
    lines.append(f"Status: {order.status.upper()}")
    
    if order.special_instructions:
        lines.append(f"Special Instructions: {order.special_instructions}")
    
    return "\n".join(lines)