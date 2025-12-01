import logging
import json
import os
from datetime import datetime
from typing import Annotated, Optional

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    RunContext,
    cli,
    function_tool,
)
from livekit.plugins import google, deepgram, silero, murf
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from pydantic import Field
from dataclasses import dataclass

from Day6.grocery_database import (
    PRODUCT_CATALOG, RECIPE_CATALOG, GroceryDB,
    search_products, find_product_by_id, find_recipe
)
from Day6.grocery_order import CartState, OrderState, OrderData, format_order_summary

load_dotenv()
logger = logging.getLogger("grocery_agent")

# --- JSON HELPER FUNCTIONS ---
ORDERS_DIR = "orders"
ORDER_HISTORY_FILE = os.path.join(ORDERS_DIR, "order_history.json")

def ensure_orders_directory():
    """Create orders directory if it doesn't exist."""
    if not os.path.exists(ORDERS_DIR):
        os.makedirs(ORDERS_DIR)

def save_order_to_json(order: OrderData) -> dict:
    """Save order to individual file and history."""
    ensure_orders_directory()
    
    # Convert order to dict
    order_dict = {
        "order_id": order.order_id,
        "timestamp": order.timestamp,
        "customer_name": order.customer_name,
        "delivery_address": order.delivery_address,
        "phone": order.phone,
        "items": order.items,
        "total_amount": order.total_amount,
        "status": order.status,
        "special_instructions": order.special_instructions
    }
    
    # Save individual order file
    order_file = os.path.join(ORDERS_DIR, f"{order.order_id}.json")
    with open(order_file, 'w') as f:
        json.dump(order_dict, f, indent=2)
    
    # Update order history
    history = []
    if os.path.exists(ORDER_HISTORY_FILE):
        with open(ORDER_HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    
    history.append(order_dict)
    
    with open(ORDER_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
    
    return order_dict

# --- USER CONTEXT ---
@dataclass
class UserContext:
    store_name: str
    catalog_info: str
    cart: CartState
    order_state: OrderState

# --- AGENT CLASS ---
class GroceryAgent(Agent):
    def __init__(self, *, userdata: UserContext) -> None:
        
        instructions = f"""
You are a friendly and helpful food & grocery ordering assistant for {userdata.store_name}.

STORE INFORMATION:
{userdata.catalog_info}

YOUR ROLE:
1. Greet customers warmly and explain what you can help with
2. Help customers find products they're looking for
3. Understand natural requests like "I need ingredients for pasta" and add all required items
4. Manage their shopping cart (add, remove, update quantities)
5. Answer questions about products, prices, and their cart
6. Place orders when customers are ready

IMPORTANT GUIDELINES:
- Be conversational and natural - don't just list tool outputs
- When customers ask for "ingredients for X", use get_recipe_ingredients first to see what's needed, then use add_recipe_to_cart to add all items at once
- Always confirm what you're adding to the cart so customers know what's happening
- Ask for clarifications when needed (size, brand, quantity)
- Keep track of their cart and remind them of items if needed
- When ready to place order, ask for: customer name, delivery address, and optionally phone number
- Be warm, friendly, and make shopping delightful!

AVAILABLE ACTIONS:
- Search for items in our catalog
- Get recipe ingredients lists
- Add individual items to cart
- Add full recipes (multiple items) to cart
- Remove items from cart
- Update item quantities
- View cart contents
- Clear entire cart
- Place order (saves to JSON file)

Remember: You're here to make grocery shopping easy and enjoyable!
"""

        super().__init__(
            instructions=instructions,
            tools=[
                # Tools will be auto-detected
            ],
        )

    @function_tool
    async def search_items(
        self,
        ctx: RunContext[UserContext],
        query: Annotated[str, Field(description="Search query for items (e.g., 'bread', 'milk', 'pizza')")]
    ) -> str:
        """
        Search for items in the catalog. Returns matching items with their IDs, names, prices, and details.
        Use this when customer asks about specific products or wants to browse items.
        """
        results = search_products(query)
        
        if not results:
            return f"No items found matching '{query}'. Try searching for: bread, milk, eggs, pasta, pizza, snacks, or prepared food."
        
        # Format results
        result_lines = [f"Found {len(results)} items matching '{query}':"]
        for product in results[:10]:  # Limit to 10 results
            result_lines.append(
                f"• {product.name} ({product.brand}, {product.size}) - ${product.price:.2f} [ID: {product.id}]"
            )
        
        return "\n".join(result_lines)

    @function_tool
    async def get_recipe_ingredients(
        self,
        ctx: RunContext[UserContext],
        recipe_name: Annotated[str, Field(description="Name of the recipe or meal (e.g., 'peanut butter sandwich', 'pasta', 'breakfast')")]
    ) -> str:
        """
        Get the list of ingredients needed for a specific recipe or meal.
        Use this when customer says things like "I need ingredients for..." or "What do I need to make..."
        """
        recipe = find_recipe(recipe_name)
        
        if not recipe:
            available_recipes = [r.name for r in RECIPE_CATALOG]
            return f"Recipe '{recipe_name}' not found. Available recipes: {', '.join(available_recipes)}"
        
        # Get products for this recipe
        ingredients = []
        for item_id in recipe.item_ids:
            product = find_product_by_id(item_id)
            if product:
                ingredients.append(
                    f"• {product.name} ({product.brand}, {product.size}) - ${product.price:.2f} [ID: {item_id}]"
                )
        
        return f"Ingredients for {recipe.name}:\n" + "\n".join(ingredients)

    @function_tool
    async def add_to_cart(
        self,
        ctx: RunContext[UserContext],
        item_id: Annotated[str, Field(description="Item ID to add (e.g., 'g001', 'p001', 's001')")],
        quantity: Annotated[int, Field(description="Quantity to add")] = 1
    ) -> str:
        """
        Add a single item to the shopping cart with specified quantity.
        Use this for adding individual products.
        """
        product = find_product_by_id(item_id)
        
        if not product:
            return f"Item with ID '{item_id}' not found in catalog. Please search for items first."
        
        # Add to cart
        cart_item = ctx.userdata.cart.add_item(
            item_id=product.id,
            name=product.name,
            quantity=quantity,
            price=product.price,
            brand=product.brand,
            size=product.size,
            category=product.category
        )
        
        item_total = cart_item.get_total()
        cart_total = ctx.userdata.cart.get_total()
        
        return (f"✅ Added {quantity}x {product.name} ({product.brand}, {product.size}) to cart - ${item_total:.2f}\n"
                f"Cart total: ${cart_total:.2f}")

    @function_tool
    async def add_recipe_to_cart(
        self,
        ctx: RunContext[UserContext],
        recipe_name: Annotated[str, Field(description="Name of the recipe to add all ingredients for")]
    ) -> str:
        """
        Add all ingredients for a recipe to the cart at once.
        Use this when customer says "get me ingredients for pasta" or similar requests.
        """
        recipe = find_recipe(recipe_name)
        
        if not recipe:
            available_recipes = [r.name for r in RECIPE_CATALOG]
            return f"Recipe '{recipe_name}' not found. Available recipes: {', '.join(available_recipes)}"
        
        # Add all items from recipe
        added_items = []
        for item_id in recipe.item_ids:
            product = find_product_by_id(item_id)
            if product:
                ctx.userdata.cart.add_item(
                    item_id=product.id,
                    name=product.name,
                    quantity=1,
                    price=product.price,
                    brand=product.brand,
                    size=product.size,
                    category=product.category
                )
                added_items.append(product.name)
        
        cart_total = ctx.userdata.cart.get_total()
        
        return (f"✅ Added ingredients for {recipe.name}: {', '.join(added_items)}\n"
                f"Cart total: ${cart_total:.2f}")

    @function_tool
    async def remove_from_cart(
        self,
        ctx: RunContext[UserContext],
        item_id: Annotated[str, Field(description="Item ID to remove from cart")]
    ) -> str:
        """
        Remove an item completely from the shopping cart.
        """
        cart_item = ctx.userdata.cart.get_item(item_id)
        
        if not cart_item:
            return f"Item '{item_id}' not found in cart."
        
        item_name = cart_item.name
        ctx.userdata.cart.remove_item(item_id)
        cart_total = ctx.userdata.cart.get_total()
        
        return f"✅ Removed {item_name} from cart. Cart total: ${cart_total:.2f}"

    @function_tool
    async def update_cart_quantity(
        self,
        ctx: RunContext[UserContext],
        item_id: Annotated[str, Field(description="Item ID to update")],
        quantity: Annotated[int, Field(description="New quantity (0 to remove item)")]
    ) -> str:
        """
        Update the quantity of an item in the cart.
        Set quantity to 0 to remove the item.
        """
        cart_item = ctx.userdata.cart.get_item(item_id)
        
        if not cart_item:
            return f"Item '{item_id}' not found in cart."
        
        item_name = cart_item.name
        
        if quantity <= 0:
            ctx.userdata.cart.remove_item(item_id)
            return f"✅ Removed {item_name} from cart."
        
        ctx.userdata.cart.update_quantity(item_id, quantity)
        cart_total = ctx.userdata.cart.get_total()
        
        return f"✅ Updated {item_name} quantity to {quantity}. Cart total: ${cart_total:.2f}"

    @function_tool
    async def view_cart(
        self,
        ctx: RunContext[UserContext]
    ) -> str:
        """
        View all items currently in the shopping cart with quantities, prices, and total.
        """
        return ctx.userdata.cart.get_summary()

    @function_tool
    async def clear_cart(
        self,
        ctx: RunContext[UserContext]
    ) -> str:
        """
        Clear all items from the shopping cart.
        Use this if customer wants to start over.
        """
        ctx.userdata.cart.clear()
        return "✅ Cart has been cleared. You can start adding items again."

    @function_tool
    async def place_order(
        self,
        ctx: RunContext[UserContext],
        customer_name: Annotated[str, Field(description="Customer's full name")],
        delivery_address: Annotated[str, Field(description="Full delivery address")],
        phone: Annotated[Optional[str], Field(description="Customer's phone number (optional)")] = None,
        special_instructions: Annotated[Optional[str], Field(description="Any special delivery or order instructions")] = None
    ) -> str:
        """
        Place the order and save it to JSON file.
        Call this when customer is done shopping and ready to checkout.
        """
        # Check if cart is empty
        if ctx.userdata.cart.is_empty():
            return "❌ Cannot place order - your cart is empty! Please add some items first."
        
        # Create order
        order = ctx.userdata.order_state.create_order(
            customer_name=customer_name,
            delivery_address=delivery_address,
            cart_items=ctx.userdata.cart.get_all_items(),
            phone=phone or "Not Provided",
            special_instructions=special_instructions or ""
        )
        
        # Save to JSON
        save_order_to_json(order)
        
        # Get order summary
        summary = format_order_summary(order)
        
        # Clear the cart
        ctx.userdata.cart.clear()
        
        return (f"🎉 Order placed successfully!\n\n{summary}\n\n"
                f"Your order will be delivered to: {delivery_address}\n"
                f"Thank you for shopping with {ctx.userdata.store_name}!")


# --- SERVER SETUP (MATCHING NYKAA PATTERN) ---
server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    """Main entry point for the grocery ordering agent."""
    
    # Store information
    store_name = "FreshMart Express"
    
    catalog_info = f"""
ABOUT {store_name}:
Your neighborhood online grocery and food ordering platform.

WHAT WE OFFER:
• Fresh Groceries: bread, eggs, milk, butter, pasta, rice, cheese, and more
• Delicious Snacks: chips, chocolates, granola bars, nuts, cookies
• Prepared Food: pizzas, sandwiches, salads, burrito bowls
• 24+ products from trusted brands
• Fast delivery within 3 days
• Fresh, high-quality products

AVAILABLE RECIPES:
We can help you get ingredients for:
- Peanut butter sandwich
- Pasta (for 1 or 2 people)
- Breakfast basics
- Cheese sandwich
- Toast with jam

Just say "I need ingredients for pasta" and we'll add everything you need!
"""
    
    # Initialize cart and order state
    cart = CartState()
    order_state = OrderState()
    
    userdata = UserContext(
        store_name=store_name,
        catalog_info=catalog_info,
        cart=cart,
        order_state=order_state
    )
    
    # Create session
    session = AgentSession[UserContext](
        userdata=userdata,
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-pro"),
        tts=murf.TTS(model="en-US-falcon"),
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )
    
    # Start session
    await session.start(agent=GroceryAgent(userdata=userdata), room=ctx.room)


if __name__ == "__main__":
    cli.run_app(server)