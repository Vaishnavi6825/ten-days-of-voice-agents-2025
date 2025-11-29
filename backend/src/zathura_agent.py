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

load_dotenv()
logger = logging.getLogger("Zathura_GM")

# --- JSON HELPER FUNCTIONS ---
JOURNAL_FILE = "zathura_journal.json"

def save_game_state(player: str, location: str, status: str, inventory: str) -> dict:
    """Saves the current game state to the JSON file."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "player": player,
        "location": location,
        "status": status,
        "inventory": inventory
    }
    
    # Load existing data or create new list
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []
        
    history.append(entry)
    
    # Write back to file
    with open(JOURNAL_FILE, "w") as f:
        json.dump(history, f, indent=4)
    
    return entry

@dataclass
class GameContext:
    story_setting: str
    game_rules: str

class ZathuraGMAgent(Agent):
    def __init__(self, *, userdata: GameContext) -> None:
        # Build dynamic context
        instructions = f"""
You are the Game Master for ZATHURA - A Space Adventure Board Game.

SETTING:
{userdata.story_setting}

RULES:
{userdata.game_rules}

YOUR ROLE:
1. Narrate the adventure. The player is in their house, but the house is floating in space.
2. Every time the player speaks, advance the story based on their choice.
3. Create dangers: Zorgon aliens, meteor showers, gravity loss.
4. **ALWAYS** end your turn by asking: "What do you do?"
5. If the player reaches a safe spot or finds an item, use the tool `log_checkpoint` to save.

STYLE:
- Retro-futuristic 1950s sci-fi aesthetic.
- Mechanical, rhythmic voice.
- Keep descriptions vivid but concise.
"""

        super().__init__(
            instructions=instructions,
            tools=[
                # Tools are auto-detected
            ],
        )

    @function_tool
    async def log_checkpoint(
        self,
        ctx: RunContext[GameContext],
        player: Annotated[str, Field(description="Name of the player")],
        location: Annotated[str, Field(description="Current location (e.g. Kitchen, Basement, Zorgon Ship)")],
        status: Annotated[str, Field(description="Current condition (e.g. Healthy, Injured, Frozen)")],
        inventory: Annotated[str, Field(description="Items the player is holding")]
    ) -> str:
        """
        Save the game state when the player finds an item, survives a danger, or reaches a new room.
        """
        save_game_state(player, location, status, inventory)
        return f"Game saved. {player} is currently in the {location}."


server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    # Build context for the agent
    story_setting = """
    The player has just started playing a vintage 1950s clockwork board game called Zathura.
    With their first move, their entire house has been launched into outer space.
    They are floating near Saturn. There are meteors, aliens (Zorgons), and malfunctioning robots.
    The only way home is to finish the game by reaching the planet Zathura.
    """

    game_rules = """
    - The game must be played to completion.
    - Cheating has severe consequences.
    - The house is the spaceship.
    - Zorgons are attracted to heat.
    """

    userdata = GameContext(
        story_setting=story_setting,
        game_rules=game_rules
    )
    
    # Configure Session
    session = AgentSession[GameContext](
        userdata=userdata,
        stt=deepgram.STT(model="nova-2"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=deepgram.TTS(
            model="aura-asteria-en",    
        ),
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )

    # --- THE FIX IS HERE ---
    # We do NOT call agent.start(). We ask the SESSION to start the agent.
    agent = ZathuraGMAgent(userdata=userdata)
    
    # Start the session with the agent
    await session.start(agent=agent, room=ctx.room)
    
    # Optional: Send the opening message manually if needed, 
    # but usually the Agent greeting handles it. 
    # If you want to force the opening line:
    await agent.say("Zathura. Game Started. Your house has just lifted off into space. A meteor is heading for the living room. Player One... what do you do?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(server)