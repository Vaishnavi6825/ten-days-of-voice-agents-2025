import logging
from typing import Annotated, Literal, Optional

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    RunContext,
    ChatContext,
    cli,
    function_tool,
)
from livekit.plugins import google, deepgram, silero, murf
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from pydantic import Field

from Day3.content_manager import ContentManager

load_dotenv()
logger = logging.getLogger("tutor-agent")
content_db = ContentManager()

# --- CONFIGURING THE 3 VOICES ---
# Note: Ensure you have these Voice IDs in Murf, or use "en-US-falcon" for all if testing.
TTS_MATTHEW = murf.TTS(model="en-US-falcon", voice="Matthew")
TTS_ALICIA = murf.TTS(model="en-US-falcon", voice="Alicia")
TTS_KEN = murf.TTS(model="en-US-falcon", voice="Ken")
TTS_ROUTER = TTS_MATTHEW 

# --- 1. THE TEACHER AGENT (Matthew) ---
class LearnAgent(Agent):
    def __init__(self, topic_id: str, chat_ctx: Optional[ChatContext] = None):
        lesson = content_db.get_lesson(topic_id)
        topic_name = lesson.title if lesson else topic_id
        summary = lesson.summary if lesson else "Content not found."
        
        super().__init__(
            instructions=f"""
            You are 'Matthew', a patient coding teacher.
            You are currently in LEARN MODE.
            Topic: {topic_name}
            Lesson: "{summary}"
            
            1. Explain the concept clearly using the lesson.
            2. Ask the user if they understand.
            3. If yes, suggest switching to QUIZ mode.
            """,
            chat_ctx=chat_ctx,
            tts=TTS_MATTHEW 
        )

# --- 2. THE QUIZ AGENT (Alicia) ---
class QuizAgent(Agent):
    def __init__(self, topic_id: str, chat_ctx: Optional[ChatContext] = None):
        lesson = content_db.get_lesson(topic_id)
        topic_name = lesson.title if lesson else topic_id
        question = lesson.sample_question if lesson else "No question."

        super().__init__(
            instructions=f"""
            You are 'Alicia', a strict but fair Quiz Master.
            You are currently in QUIZ MODE.
            Topic: {topic_name}
            Question: "{question}"
            
            1. Ask the question immediately.
            2. Wait for the answer.
            3. If right, congratulate them. 
            4. If wrong, CORRECT them.
            """,
            chat_ctx=chat_ctx,
            tts=TTS_ALICIA 
        )

# --- 3. THE STUDENT AGENT (Ken) ---
class TeachBackAgent(Agent):
    def __init__(self, topic_id: str, chat_ctx: Optional[ChatContext] = None):
        lesson = content_db.get_lesson(topic_id)
        topic_name = lesson.title if lesson else topic_id

        super().__init__(
            instructions=f"""
            You are 'Ken', a student who needs help.
            You are currently in TEACH-BACK MODE.
            Topic: {topic_name}
            
            1. Act confused. Say: "I don't understand {topic_name}. Can you explain it to me?"
            2. Listen to their explanation.
            3. Evaluate:
               - If they explain well, say: "Aha! I get it now! You're a great teacher."
               - If they are wrong, politely correct them.
            """,
            chat_ctx=chat_ctx,
            tts=TTS_KEN 
        )

# --- 4. THE ROUTER AGENT ---
class RouterAgent(Agent):
    def __init__(self, chat_ctx: Optional[ChatContext] = None):
        topics = content_db.get_all_topics()
        super().__init__(
            instructions=f"""
            You are the main receptionist for the Coding Academy.
            
            Available Topics: {topics}
            Available Modes: Learn, Quiz, Teach-Back.
            
            1. Greet the user warmly.
            2. Ask them to pick a Topic AND a Mode.
            3. Use the 'switch_mode_tool' to transfer them to a specialist.
            """,
            chat_ctx=chat_ctx,
            tts=TTS_ROUTER 
        )

    @function_tool
    async def switch_mode_tool(
        self,
        ctx: RunContext,
        mode: Annotated[Literal["learn", "quiz", "teach_back"], Field(description="The learning mode.")],
        topic: Annotated[Literal["variables", "loops", "functions"], Field(description="The topic ID.")]
    ):
        """Switch the agent's personality and mode based on the user's request."""
        
        logger.info(f"Transferring to {mode} for {topic}")
        
        # --- THE FIX IS HERE ---
        # We access chat_ctx from 'self' (the current Agent), not the session.
        current_history = self.chat_ctx.copy()

        if mode == "learn":
            return LearnAgent(topic, chat_ctx=current_history), f"Switching to Learn Mode for {topic}"
        elif mode == "quiz":
            return QuizAgent(topic, chat_ctx=current_history), f"Switching to Quiz Mode for {topic}"
        elif mode == "teach_back":
            return TeachBackAgent(topic, chat_ctx=current_history), f"Switching to Teach-Back Mode for {topic}"
        
        return self, "Stay"

server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    # Start with the Router
    agent = RouterAgent()
    
    # Enable the tools
    agent.tools.append(agent.switch_mode_tool)
    LearnAgent.tools = [agent.switch_mode_tool]
    QuizAgent.tools = [agent.switch_mode_tool]
    TeachBackAgent.tools = [agent.switch_mode_tool]

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-pro"),
        tts=TTS_ROUTER, 
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )

    await session.start(agent=agent, room=ctx.room)

if __name__ == "__main__":
    cli.run_app(server)