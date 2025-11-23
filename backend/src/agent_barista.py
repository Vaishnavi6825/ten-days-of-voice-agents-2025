import logging
import os
import sys
import json  # <--- Added for JSON export
from datetime import datetime # <--- Added for timestamps
from typing import Annotated, Literal, List

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    RunContext,
    ToolError,
    cli,
    function_tool,
)
from livekit.plugins import google, deepgram, silero, murf
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from pydantic import Field
from dataclasses import dataclass

# Import our custom modules
from database import (
    COMMON_INSTRUCTIONS,
    FakeDB,
    MenuItem,
    find_items_by_id,
    menu_instructions,
)
from order import OrderedDrink, OrderState

load_dotenv()
logger = logging.getLogger("coffee-barista")

@dataclass
class Userdata:
    order: OrderState
    drink_items: list[MenuItem]
    milk_items: list[MenuItem]
    extra_items: list[MenuItem]

class CoffeeShopAgent(Agent):
    def __init__(self, *, userdata: Userdata) -> None:
        instructions = (
            COMMON_INSTRUCTIONS
            + "\n\n"
            + menu_instructions("drinks", userdata.drink_items)
            + "\n\n"
            + menu_instructions("milks", userdata.milk_items)
            + "\n\n"
            + menu_instructions("extras/syrups", userdata.extra_items)
            + "\n\n"
            + "Available sizes: Small (s), Medium (m), Large (l), Extra Large (xl)."
        )

        super().__init__(
            instructions=instructions,
            tools=[
                
            ],
        )

    @function_tool
    async def order_drink_tool(
        self,
        ctx: RunContext[Userdata],
        drink_id: Annotated[
            str, Field(description="The ID of the drink (e.g., 'latte', 'cappuccino').")
        ],
        size: Annotated[
            Literal["s", "m", "l", "xl"], 
            Field(description="The size of the drink.")
        ] = "m",
        milk_id: Annotated[
            str, Field(description="Optional ID for milk preference (e.g., 'oat_milk').")
        ] = None,
        extra_id: Annotated[
            str, Field(description="Optional ID for syrup or extra (e.g., 'vanilla').")
        ] = None,
    ) -> str:
        """
        Use this tool when the user wants to order a coffee or drink. 
        If the user asks for 'Oat Latte', map it to drink_id='latte' and milk_id='oat_milk' unless 'oat_latte' exists.
        """
        valid_drink = find_items_by_id(ctx.userdata.drink_items, drink_id)
        if not valid_drink:
            raise ToolError(f"Drink '{drink_id}' not found on menu.")

        if milk_id:
            valid_milk = find_items_by_id(ctx.userdata.milk_items, milk_id)
            if not valid_milk:
                raise ToolError(f"Milk type '{milk_id}' not found.")
        
        extras = []
        if extra_id:
            valid_extra = find_items_by_id(ctx.userdata.extra_items, extra_id)
            if not valid_extra:
                raise ToolError(f"Extra '{extra_id}' not found.")
            extras.append(extra_id)

        item = OrderedDrink(
            drink_id=drink_id,
            size=size,
            milk_id=milk_id,
            syrup_ids=extras
        )
        
        await ctx.userdata.order.add(item)
        
        description = f"Added {size.upper()} {valid_drink.name}"
        if milk_id: description += f" with {milk_id.replace('_', ' ')}"
        if extra_id: description += f" and {extra_id.replace('_', ' ')}"
        
        return description

    @function_tool
    async def remove_item_tool(
        self, 
        ctx: RunContext[Userdata],
        order_id: Annotated[str, Field(description="The UUID of the order item to remove.")]
    ) -> str:
        """Remove an item from the order."""
        try:
            removed = await ctx.userdata.order.remove(order_id)
            return f"Removed item: {removed.drink_id}"
        except ValueError:
            return "Item not found."

    @function_tool
    async def confirm_order_tool(self, ctx: RunContext[Userdata]) -> str:
        """List all items currently in the cart to confirm with user."""
        items = ctx.userdata.order.items.values()
        if not items:
            return "The order is currently empty."
        
        report = "Current Order:\n"
        for i in items:
            report += f"- {i.size} {i.drink_id} (Milk: {i.milk_id}, Extras: {i.syrup_ids}) [ID: {i.order_id}]\n"
        return report

async def new_userdata() -> Userdata:
    fake_db = FakeDB()
    return Userdata(
        order=OrderState(),
        drink_items=await fake_db.list_drinks(),
        milk_items=await fake_db.list_milks(),
        extra_items=await fake_db.list_extras(),
    )

server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    userdata = await new_userdata()
    
    session = AgentSession[Userdata](
        userdata=userdata,
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-pro"),
        tts=murf.TTS(model="en-US-falcon"),
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )

    await session.start(agent=CoffeeShopAgent(userdata=userdata), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(server)