import logging
import json
import os
from datetime import datetime
from typing import Annotated

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
logger = logging.getLogger("wellness-companion")

# --- JSON HELPER FUNCTIONS ---
JSON_FILE = "wellness_log.json"

def get_last_checkin():
    """Reads the JSON file and returns the last entry if it exists."""
    if not os.path.exists(JSON_FILE):
        return None
    
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            if data:
                return data[-1] # Return the last item in the list
    except Exception:
        return None
    return None

def save_checkin_to_json(mood: str, goals: list, summary: str):
    """Saves the current check-in to the JSON file."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "mood": mood,
        "goals": goals,
        "summary": summary
    }
    
    # Load existing data or create new list
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []
        
    history.append(entry)
    
    # Write back to file
    with open(JSON_FILE, "w") as f:
        json.dump(history, f, indent=4)
    
    return entry

@dataclass
class Userdata:
    last_session_summary: str

class WellnessAgent(Agent):
    def __init__(self, *, userdata: Userdata) -> None:
        # 1. Build the dynamic context based on history
        context_str = ""
        if userdata.last_session_summary:
            context_str = f"CONTEXT FROM LAST SESSION: {userdata.last_session_summary}\n(Use this to welcome the user back, e.g., 'Last time you felt...')"
        else:
            context_str = "This is the user's first session. Welcome them warmly."

        # 2. Define the System Prompt
        instructions = f"""
        You are a supportive, grounded Health & Wellness Voice Companion.
        
        {context_str}

        YOUR GOAL:
        1. Ask the user about their MOOD and ENERGY (e.g., "How are you feeling today?").
        2. Ask about their INTENTIONS/GOALS for today (limit to 1-3 simple things).
        3. Offer brief, grounded encouragement (no medical advice).
        4. CRITICAL: Before saying goodbye, you MUST use the 'save_daily_checkin' tool to save the conversation.
        
        Once the check-in is saved, confirm it to the user and wish them well.
        """

        super().__init__(
            instructions=instructions,
            tools=[
                # Tools are auto-detected
            ],
        )

    @function_tool
    async def save_daily_checkin(
        self,
        ctx: RunContext[Userdata],
        mood: Annotated[str, Field(description="The user's self-reported mood and energy levels.")],
        goals: Annotated[list[str], Field(description="A list of 1-3 goals the user mentioned.")],
        summary: Annotated[str, Field(description="A brief 1-sentence summary of the check-in.")]
    ) -> str:
        """
        Call this tool at the END of the conversation to save the user's data to the JSON file.
        """
        save_checkin_to_json(mood, goals, summary)
        return "Check-in saved successfully to wellness_log.json."


server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    # 1. Read JSON history before starting
    last_entry = get_last_checkin()
    history_summary = ""
    if last_entry:
        history_summary = f"Date: {last_entry['timestamp']}, Mood: {last_entry['mood']}, Goals: {last_entry['goals']}"

    userdata = Userdata(last_session_summary=history_summary)
    
    session = AgentSession[Userdata](
        userdata=userdata,
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-pro"),
        tts=murf.TTS(model="en-US-falcon"), # REQUIRED for the challenge
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )

    await session.start(agent=WellnessAgent(userdata=userdata), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(server)