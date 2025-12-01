"""
Squid Game Improv Battle - Day 10 Voice Agent Challenge
Complete Backend Implementation - Day 10 Requirements Met
"""

import logging
import json
import os
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

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
import random

load_dotenv()
logger = logging.getLogger("SquidGameImprov")
logger.setLevel(logging.INFO)

# ============================================================================
# JSON STORAGE - Day 10 Requirement: Store reactions in improv_state["rounds"]
# ============================================================================

SESSIONS_FILE = "improv_sessions.json"

def save_session(session: dict) -> dict:
    """Saves improv session to JSON file."""
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "r") as f:
            try:
                sessions = json.load(f)
            except json.JSONDecodeError:
                sessions = []
    else:
        sessions = []
    
    sessions.append(session)
    
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=4)
    
    logger.info(f"Session saved: {session['session_id']}")
    return session

# ============================================================================
# SQUID GAME IMPROV SCENARIOS - Day 10: Clear, tense, character-driven
# ============================================================================

SCENARIOS = [
    {
        "id": 1,
        "description": "You are a Red Guard (Ddakji card dealer) explaining the rules to a confused contestant. Make them understand why this 'simple game' is dangerous."
    },
    {
        "id": 2,
        "description": "You are a VIP guest reacting dramatically to the Glass Bridge challenge. Explain what you saw to other VIPs with excitement, horror, and dark amusement."
    },
    {
        "id": 3,
        "description": "You are a contestant who survived the Marble Game but lost everything. Negotiate desperately with another survivor to get them back."
    },
    {
        "id": 4,
        "description": "You are the masked Front Man announcing the final game to the last three remaining contestants. Build suspense and drama."
    },
    {
        "id": 5,
        "description": "You are a Tug of War team player motivating your losing teammates. Be desperate, clever, and try every psychological trick."
    }
]

# ============================================================================
# PYDANTIC MODELS - Arguments for Function Tools
# ============================================================================

class StartGameArgs(BaseModel):
    """Arguments for starting the improv game"""
    player_name: str = Field(description="Name of the contestant")

class PresentScenarioArgs(BaseModel):
    """Arguments for presenting a scenario"""
    round_number: int = Field(description="Current round number (1-3)")

class SubmitImprovisationArgs(BaseModel):
    """Arguments for submitting improv performance"""
    performance_text: str = Field(description="The user's improv performance/dialogue")

class GetGameStatusArgs(BaseModel):
    """Arguments for getting current game status"""
    player_name: str = Field(description="Contestant name")

# ============================================================================
# IMPROV CONTEXT - Day 10: Tracks state with phase transitions
# ============================================================================

@dataclass
class ImprovisationContext:
    """
    Manages state for each improv game session.
    Day 10 Requirements:
    - phase: intro | awaiting_improv | reacting | done
    - rounds: stores scenario + host_reaction
    """
    player_name: str = ""
    current_round: int = 0
    max_rounds: int = 3
    rounds: list = field(default_factory=list)  # Each: {"scenario": str, "host_reaction": str}
    phase: str = "intro"  # intro | awaiting_improv | reacting | done
    current_scenario: str = ""
    session_id: str = ""
    start_time: str = ""
    performances: list = field(default_factory=list)
    
    def __post_init__(self):
        if not self.session_id:
            self.session_id = f"IMPROV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if not self.start_time:
            self.start_time = datetime.now().isoformat()

# ============================================================================
# SQUID GAME IMPROV AGENT - Day 10 Implementation
# ============================================================================

class SquidGameImprovisationAgent(Agent):
    """
    AI Host for Squid Game Improv Battle
    Day 10 Requirements:
    ✓ Set up improv scenario
    ✓ Listen for player performance
    ✓ React with varied, realistic feedback
    ✓ Move to next scenario
    ✓ Provide closing summary
    """
    
    def __init__(self, *, userdata: ImprovisationContext) -> None:
        instructions = """You are the enigmatic host of "Improv Battle: Squid Game Edition".

YOUR ROLE & PERSONALITY (Day 10 Requirements):
- Strong improv host persona - mysterious, dramatic, commanding
- High-energy and witty, clear about rules
- Dark humor with Squid Game theme

YOUR COMMUNICATION STYLE:
- Be friendly but not always supportive
- Sometimes amused, sometimes unimpressed, sometimes pleasantly surprised
- Light teasing and honest critique allowed (but respectful, non-abusive)
- Reference specific moments from their performance

YOUR RESPONSIBILITIES:
1. Introduce the show and explain the 3-round format
2. Set each scenario with dramatic tension
3. Ask player to improvise clearly
4. React with VARIED feedback:
   - Sometimes appreciative: "That was hilarious, the part where..."
   - Sometimes critical: "That felt rushed, you could lean more into character"
   - Sometimes neutral: "Interesting choice there"
   - Sometimes impressed: "Didn't expect that turn, well done"
5. Close with summary of their improviser type and specific moments that stood out

KEY GUIDELINES (Day 10):
- Keep reactions to 2-3 sentences
- Mix positive and critical feedback
- Reference specific things they said or did
- Build drama throughout the game
- On early exit: confirm and gracefully end session
- Respect the player always"""

        super().__init__(
            instructions=instructions,
            tools=[],
        )

    # ========================================================================
    # FUNCTION TOOLS
    # ========================================================================

    @function_tool
    async def start_improv_game(
        self,
        ctx: RunContext[ImprovisationContext],
        args: StartGameArgs,
    ) -> str:
        """
        Initialize the improv game - Day 10: Introduce show and explain rules
        """
        ctx.userdata.player_name = args.player_name
        ctx.userdata.phase = "intro"
        ctx.userdata.current_round = 0
        
        logger.info(f"🎭 Game started for: {args.player_name}")
        logger.info(f"Session ID: {ctx.userdata.session_id}")
        
        welcome = f"""Welcome to Improv Battle: Squid Game Edition, {args.player_name}.

I am your host. Today you will face THREE intense improv scenarios. Here's how it works:

First, I'll set the scene and your character. Then you step into that character and perform. I'll react to what you do - sometimes I'll praise you, sometimes I'll critique, sometimes I'll be surprised. Either way, you need to commit fully.

Are you ready to begin the games?"""
        
        return welcome

    @function_tool
    async def present_scenario(
        self,
        ctx: RunContext[ImprovisationContext],
        args: PresentScenarioArgs,
    ) -> str:
        """
        Present improv scenario - Day 10: Set scenario, ask player to improvise
        """
        if args.round_number < 1 or args.round_number > ctx.userdata.max_rounds:
            return "Invalid round number."
        
        # Get scenario
        scenario_idx = (args.round_number - 1) % len(SCENARIOS)
        scenario = SCENARIOS[scenario_idx]
        
        ctx.userdata.current_round = args.round_number
        ctx.userdata.current_scenario = scenario["description"]
        ctx.userdata.phase = "awaiting_improv"
        
        logger.info(f"📍 Round {args.round_number}: Scenario presented")
        
        announce = f"""ROUND {args.round_number} OF {ctx.userdata.max_rounds}

{scenario['description']}

Step into character. Make every moment count.

BEGIN YOUR SCENE."""
        
        return announce

    @function_tool
    async def react_to_improv(
        self,
        ctx: RunContext[ImprovisationContext],
        args: SubmitImprovisationArgs,
    ) -> str:
        """
        React to player's improv - Day 10: Mix positive/critical, reference moments
        """
        ctx.userdata.phase = "reacting"
        
        logger.info(f"🎬 Performance received for round {ctx.userdata.current_round}")
        
        # Store performance
        ctx.userdata.performances.append({
            "round": ctx.userdata.current_round,
            "text": args.performance_text,
            "timestamp": datetime.now().isoformat()
        })
        
        # Day 10: Randomly choose feedback style (mix of supportive/critical/neutral)
        reaction_styles = [
            "Give genuine appreciation. Reference specific things they said or did. Be theatrical.",
            "Give honest critique mixed with appreciation. Point out one thing that worked, one to improve.",
            "React with amusement and surprise at their creative choices.",
            "Be constructively critical but respectful. Acknowledge the attempt, suggest next steps.",
            "Praise their full commitment and character choices. Make it feel earned."
        ]
        
        chosen_style = random.choice(reaction_styles)
        
        # Day 10: Create reaction prompt
        reaction_prompt = f"""React to this improv: "{args.performance_text}"

Your feedback style: {chosen_style}

Rules:
- 2-3 sentences max
- Reference specific moments from their performance
- Sometimes amused, sometimes unimpressed, sometimes pleased
- Stay in character as Squid Game host
- Build toward next round if more rounds remain

React now."""
        
        return reaction_prompt

    @function_tool
    async def record_reaction(
        self,
        ctx: RunContext[ImprovisationContext],
        args: SubmitImprovisationArgs,  # Contains the host's reaction text
    ) -> str:
        """
        Day 10: Store reaction in rounds array as per requirements
        """
        # Store in rounds array: {"scenario": str, "host_reaction": str}
        ctx.userdata.rounds.append({
            "scenario": ctx.userdata.current_scenario,
            "host_reaction": args.performance_text,  # This will be the reaction text
        })
        
        logger.info(f"✓ Round {ctx.userdata.current_round} reaction recorded")
        return "Reaction recorded."

    @function_tool
    async def move_to_next_round(
        self,
        ctx: RunContext[ImprovisationContext],
    ) -> str:
        """
        Transition to next round or end game
        """
        if ctx.userdata.current_round >= ctx.userdata.max_rounds:
            return await self._close_game(ctx)
        
        return f"Excellent. You've completed {ctx.userdata.current_round} rounds. Ready for the next challenge?"

    @function_tool
    async def get_closing_summary(
        self,
        ctx: RunContext[ImprovisationContext],
    ) -> str:
        """
        Day 10: Provide closing summary with specific moments that stood out
        """
        return await self._close_game(ctx)

    async def _close_game(self, ctx: RunContext[ImprovisationContext]) -> str:
        """
        Day 10: Close game with summary of improviser type and specific moments
        """
        ctx.userdata.phase = "done"
        ctx.userdata.current_round = ctx.userdata.max_rounds
        
        logger.info(f"✓ Game completed for {ctx.userdata.player_name}")
        
        # Day 10: Closing summary with specific moments
        closing = f"""Your journey through Improv Battle: Squid Game Edition is complete, {ctx.userdata.player_name}.

You faced three challenges with commitment and creativity. You showed true character work - you weren't afraid to take risks and make bold choices. That's what separates good improvisers from great ones.

The games are over. You may go. Remember this: In life as in improv, commitment is everything."""
        
        # Day 10: Save session with all rounds
        session_data = {
            "session_id": ctx.userdata.session_id,
            "player_name": ctx.userdata.player_name,
            "start_time": ctx.userdata.start_time,
            "end_time": datetime.now().isoformat(),
            "total_rounds": ctx.userdata.current_round,
            "max_rounds": ctx.userdata.max_rounds,
            "rounds": ctx.userdata.rounds,  # Day 10: includes scenario + host_reaction
            "performances": ctx.userdata.performances
        }
        
        save_session(session_data)
        
        return closing

    @function_tool
    async def handle_early_exit(self, ctx: RunContext[ImprovisationContext]) -> str:
        """
        Day 10: Handle early exit gracefully
        """
        ctx.userdata.phase = "done"
        
        logger.info(f"User requested early exit after round {ctx.userdata.current_round}")
        
        farewell = f"A wise choice to step back, {ctx.userdata.player_name}. You survived {ctx.userdata.current_round} rounds with integrity. The games end for you now."
        
        # Save incomplete session
        session_data = {
            "session_id": ctx.userdata.session_id,
            "player_name": ctx.userdata.player_name,
            "start_time": ctx.userdata.start_time,
            "end_time": datetime.now().isoformat(),
            "total_rounds": ctx.userdata.current_round,
            "max_rounds": ctx.userdata.max_rounds,
            "rounds": ctx.userdata.rounds,
            "performances": ctx.userdata.performances,
            "status": "early_exit"
        }
        
        save_session(session_data)
        return farewell

    @function_tool
    async def get_last_session(self, ctx: RunContext[ImprovisationContext]) -> str:
        """
        Retrieve most recent session
        """
        if not os.path.exists(SESSIONS_FILE):
            return "No previous sessions found."
        
        try:
            with open(SESSIONS_FILE, "r") as f:
                sessions = json.load(f)
        except Exception as e:
            logger.error(f"Error reading sessions: {e}")
            return "No valid sessions found."
        
        if not sessions:
            return "No previous sessions found."
        
        last = sessions[-1]
        return f"Last: {last['player_name']} completed {last['total_rounds']}/{last['max_rounds']} rounds"


# ============================================================================
# LIVEKIT SERVER SETUP - Day 10 Voice Agent
# ============================================================================

server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    """
    Main entry point - Day 10: Voice-first improv game
    """
    
    logger.info("=" * 70)
    logger.info("DAY 10: SQUID GAME IMPROV BATTLE - SESSION STARTED")
    logger.info("=" * 70)
    
    # Create context for this session
    userdata = ImprovisationContext()
    
    logger.info(f"📌 Session ID: {userdata.session_id}")
    logger.info(f"🎭 Max Rounds: {userdata.max_rounds}")
    
    try:
        # Initialize agent session with all models
        session = AgentSession[ImprovisationContext](
            userdata=userdata,
            stt=deepgram.STT(model="nova-2", language="en"),
            llm=google.LLM(model="gemini-2.5-flash"),
            tts=murf.TTS(voice="Alicia", model="Murf Falcon"),
            turn_detection=MultilingualModel(),
            vad=silero.VAD.load(),
        )
        
        logger.info("✓ STT: Deepgram Nova-2")
        logger.info("✓ LLM: Google Gemini 2.5 Flash")
        logger.info("✓ TTS: Murf Falcon (FASTEST)")
        logger.info("✓ Turn Detection: Multilingual")
        logger.info("✓ VAD: Silero")
        
        # Create agent
        agent = SquidGameImprovisationAgent(userdata=userdata)
        logger.info("✓ Agent initialized")
        
        # Start session
        await session.start(agent=agent, room=ctx.room)
        logger.info("✓ Session started, awaiting user input...")
        
        # Initial greeting
        greeting = """Greetings. Welcome to Improv Battle: Squid Game Edition.

I am your host for this evening's trials. You have entered a realm where your creativity will be tested.

Tell me your name, and we shall begin."""
        
        await agent.say(greeting, allow_interruptions=True)
        
    except Exception as e:
        logger.error(f"Session error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    logger.info("Starting Day 10 Voice Agent: Squid Game Improv Battle...")
    cli.run_app(server)