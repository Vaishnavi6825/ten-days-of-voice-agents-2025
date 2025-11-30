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
from pydantic import BaseModel, Field
from dataclasses import dataclass

load_dotenv()
logger = logging.getLogger("EcommerceGM")

# --- JSON HELPER FUNCTIONS ---
ORDERS_FILE = "orders.json"

def save_order(order: dict) -> dict:
    """Saves order to JSON file."""
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            try:
                orders = json.load(f)
            except json.JSONDecodeError:
                orders = []
    else:
        orders = []
    
    orders.append(order)
    
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)
    
    return order

# --- PYDANTIC MODELS ---
class SearchProductsArgs(BaseModel):
    """Arguments for searching products"""
    query: str = Field(default="", description="Search query or product name (e.g., 'mugs', 'tshirts')")
    category: str = Field(default="", description="Product category (e.g., 'mug', 'hoodie', 't-shirt')")
    max_price: int = Field(default=999999, description="Maximum price filter in INR")
    color: str = Field(default="", description="Color filter if applicable")

class PlaceOrderArgs(BaseModel):
    """Arguments for placing an order"""
    product_index: int = Field(description="Index of product from last search results (1-based)")
    quantity: int = Field(default=1, description="Quantity to order")
    size: str = Field(default="", description="Size if applicable (e.g., 'M', 'L', 'XL')")
    color: str = Field(default="", description="Color if applicable")

@dataclass
class EcommerceContext:
    catalog: list
    conversation_history: list = None
    current_browsing: list = None
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
        if self.current_browsing is None:
            self.current_browsing = []

class EcommerceAgent(Agent):
    def __init__(self, *, userdata: EcommerceContext) -> None:
        instructions = """
You are an AI Shopping Assistant for our ACP-compliant e-commerce platform.

YOUR ROLE:
1. Help customers browse our product catalog using natural language queries.
2. When a user asks for products, use the search_products tool with their query.
3. Summarize search results with product name, price, and key details.
4. When a user wants to buy, use the place_order tool to create an order.
5. Confirm order details with order ID and total price.
6. If asked about the last order, use the get_last_order tool.

COMMUNICATION STYLE:
- Be friendly and helpful.
- Always mention product names and prices clearly.
- Ask clarifying questions if needed (e.g., "Which size would you like?").
- Confirm every order before finalizing.

IMPORTANT: Always provide all required parameters to functions. Use empty strings or default values for optional fields.
"""

        super().__init__(
            instructions=instructions,
            tools=[],
        )

    def _normalize_text(self, text: str) -> str:
        """Helper to normalize text for fuzzy matching (removes punctuation/hyphens)"""
        if not text: return ""
        # Replace hyphens with spaces (t-shirt -> t shirt)
        text = text.lower().replace("-", " ").replace(",", " ")
        return text

    @function_tool
    async def search_products(
        self,
        ctx: RunContext[EcommerceContext],
        args: SearchProductsArgs,
    ) -> str:
        """
        Search the product catalog based on user preferences.
        Returns a formatted list of matching products.
        """
        results = []
        
        # Normalize inputs
        query_text = self._normalize_text(args.query)
        category_text = self._normalize_text(args.category)
        color_text = self._normalize_text(args.color)
        
        # Split query into keywords for smarter matching
        query_keywords = query_text.split() if query_text else []

        for product in ctx.userdata.catalog:
            # 1. Check Category
            if category_text:
                prod_cat = self._normalize_text(product.get("category", ""))
                # Allow partial match (e.g., "tshirt" matches "t-shirt")
                if category_text not in prod_cat and prod_cat not in category_text:
                    continue
            
            # 2. Check Price
            if args.max_price and args.max_price < 999999:
                if product.get("price", 0) > args.max_price:
                    continue
            
            # 3. Check Color
            if color_text:
                prod_color = self._normalize_text(product.get("color", ""))
                if color_text not in prod_color:
                    continue
            
            # 4. Smart Text Search (The Fix)
            if query_keywords:
                # Combine all searchable text from the product
                prod_text = self._normalize_text(
                    f"{product.get('name', '')} {product.get('description', '')} {product.get('category', '')}"
                )
                
                # Check if ALL keywords match (fuzzy)
                match_all = True
                for word in query_keywords:
                    # Handle plurals simply: "mugs" -> "mug"
                    singular_word = word[:-1] if word.endswith('s') and len(word) > 3 else word
                    
                    if singular_word not in prod_text:
                        match_all = False
                        break
                
                if not match_all:
                    continue
            
            results.append(product)
        
        # Store results
        ctx.userdata.current_browsing = results
        
        if not results:
            return f"Sorry, I couldn't find any products matching '{args.query}'. Try specific terms like 'coffee mug', 'hoodie', or 'white t-shirt'."
        
        # Format results
        response = f"Great! I found {len(results)} product(s):\n\n"
        for idx, product in enumerate(results, 1):
            response += f"{idx}. {product['name']}\n"
            response += f"   Price: ₹{product['price']}\n"
            if product.get("color"):
                response += f"   Color: {product['color']}\n"
            if product.get("size"):
                response += f"   Sizes: {product['size']}\n"
            response += f"   {product.get('description', '')}\n\n"
        
        return response

    @function_tool
    async def place_order(
        self,
        ctx: RunContext[EcommerceContext],
        args: PlaceOrderArgs,
    ) -> str:
        """
        Place an order for a specific product.
        """
        if not ctx.userdata.current_browsing:
            return "Please search for products first before placing an order."
        
        if args.product_index < 1 or args.product_index > len(ctx.userdata.current_browsing):
            return f"Invalid selection. Please choose 1-{len(ctx.userdata.current_browsing)}."
        
        product = ctx.userdata.current_browsing[args.product_index - 1]
        
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        total_price = product["price"] * args.quantity
        
        order = {
            "order_id": order_id,
            "timestamp": datetime.now().isoformat(),
            "items": [
                {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "quantity": args.quantity,
                    "unit_price": product["price"],
                    "size": args.size if args.size else "N/A",
                    "color": args.color if args.color else product.get("color", "N/A"),
                }
            ],
            "total": total_price,
            "currency": "INR",
        }
        
        save_order(order)
        
        return f"""
🎉 Order Confirmed!
Order ID: {order_id}
Product: {product['name']}
Total: ₹{total_price}
"""

    @function_tool
    async def get_last_order(self, ctx: RunContext[EcommerceContext]) -> str:
        """Retrieve the most recent order."""
        if not os.path.exists(ORDERS_FILE):
            return "No previous orders found."
        
        try:
            with open(ORDERS_FILE, "r") as f:
                orders = json.load(f)
        except:
            return "No valid orders found."
        
        if not orders:
            return "No previous orders found."
        
        last = orders[-1]
        item = last["items"][0]
        return f"Your last order was {item['product_name']} for ₹{last['total']}."


server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    from ecommerce_catalog import PRODUCTS
    
    userdata = EcommerceContext(catalog=PRODUCTS)
    
    session = AgentSession[EcommerceContext](
        userdata=userdata,
        stt=deepgram.STT(model="nova-2"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="Alicia",
            model="Murf Falcon",
        ),
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )

    agent = EcommerceAgent(userdata=userdata)
    await session.start(agent=agent, room=ctx.room)
    
    await agent.say("Welcome! I can help you find coffee mugs, t-shirts, and hoodies. What would you like to buy?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(server)