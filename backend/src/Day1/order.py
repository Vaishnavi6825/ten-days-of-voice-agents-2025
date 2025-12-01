# order.py
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid

class OrderedItem(BaseModel):
    """Base class for ordered items."""
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class OrderedDrink(OrderedItem):
    """A coffee drink order."""
    drink_id: str
    size: Optional[str] = "m" # Default to medium
    milk_id: Optional[str] = None
    syrup_ids: List[str] = [] # Can have multiple syrups
    notes: Optional[str] = None

class OrderState:
    """Manages the current order state."""
    
    def __init__(self, items: dict = None):
        self.items: dict[str, OrderedItem] = items or {}
    
    async def add(self, item: OrderedItem) -> None:
        """Add an item to the order."""
        self.items[item.order_id] = item
    
    async def remove(self, order_id: str) -> OrderedItem:
        if order_id not in self.items:
            raise ValueError(f"Item with order_id {order_id} not found")
        return self.items.pop(order_id)
    
    def clear(self) -> None:
        self.items.clear()