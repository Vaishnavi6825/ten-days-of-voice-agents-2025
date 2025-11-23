# database.py
from dataclasses import dataclass
from typing import List, Optional

# --- Configuration ---
COMMON_INSTRUCTIONS = """
You are a friendly and helpful barista at a premium coffee shop.
Your job is to take orders and make customers feel welcome.
You should always confirm the size of the drink.
If they don't specify milk or syrup, assume they don't want any, but you can suggest it.
"""

@dataclass
class MenuItem:
    id: str
    name: str
    category: str  # drink, milk, syrup, size
    price: float = 0.0

# --- Data ---
# We convert your dict into a list of objects so the agent can filter them
raw_data = [
    # Drinks
    MenuItem("espresso", "Espresso", "drink"),
    MenuItem("americano", "Americano", "drink"),
    MenuItem("cappuccino", "Cappuccino", "drink"),
    MenuItem("latte", "Latte", "drink"),
    MenuItem("macchiato", "Macchiato", "drink"),
    MenuItem("flat_white", "Flat White", "drink"),
    MenuItem("cortado", "Cortado", "drink"),
    MenuItem("mocha", "Mocha", "drink"),
    MenuItem("oat_latte", "Oat Milk Latte", "drink"),
    MenuItem("cold_brew", "Cold Brew", "drink"),
    
    # Sizes
    MenuItem("s", "Small (8oz)", "size"),
    MenuItem("m", "Medium (12oz)", "size"),
    MenuItem("l", "Large (16oz)", "size"),
    MenuItem("xl", "Extra Large (20oz)", "size"),

    # Milk Options
    MenuItem("reg_milk", "Regular Milk", "milk"),
    MenuItem("oat_milk", "Oat Milk", "milk"),
    MenuItem("almond_milk", "Almond Milk", "milk"),
    MenuItem("soy_milk", "Soy Milk", "milk"),
    MenuItem("coco_milk", "Coconut Milk", "milk"),
    MenuItem("lactose_free", "Lactose-free", "milk"),

    # Extras/Syrups
    MenuItem("shot", "Extra Shot", "extra"),
    MenuItem("vanilla", "Vanilla Syrup", "extra"),
    MenuItem("caramel", "Caramel Syrup", "extra"),
    MenuItem("hazelnut", "Hazelnut Syrup", "extra"),
    MenuItem("honey", "Honey", "extra"),
    MenuItem("sugar", "Sugar", "extra"),
    MenuItem("cinnamon", "Cinnamon", "extra"),
    MenuItem("whip", "Whipped Cream", "extra"),
]

class FakeDB:
    async def list_drinks(self) -> List[MenuItem]:
        return [i for i in raw_data if i.category == "drink"]

    async def list_milks(self) -> List[MenuItem]:
        return [i for i in raw_data if i.category == "milk"]
    
    async def list_extras(self) -> List[MenuItem]:
        return [i for i in raw_data if i.category == "extra"]

# Helper to find items
def find_items_by_id(items: List[MenuItem], item_id: str) -> Optional[MenuItem]:
    for item in items:
        if item.id == item_id:
            return item
    return None

def menu_instructions(category: str, items: List[MenuItem]) -> str:
    item_names = ", ".join([f"{i.name} ({i.id})" for i in items])
    return f"Available {category}: {item_names}"