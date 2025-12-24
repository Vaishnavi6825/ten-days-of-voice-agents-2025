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
from todoist_api_python.api import TodoistAPI

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
        You are a supportive, grounded Health & Wellness Voice Companion with advanced capabilities.
        
        {context_str}

        YOUR CORE GOAL:
        1. Ask the user about their MOOD and ENERGY (e.g., "How are you feeling today?").
        2. Ask about their INTENTIONS/GOALS for today (limit to 1-3 simple things).
        3. Offer brief, grounded encouragement (no medical advice).
        4. CRITICAL: Before saying goodbye, you MUST use the 'save_daily_checkin' tool to save the conversation.
        
        ADVANCED CAPABILITIES:
        - When user mentions goals/tasks, offer to create them in Todoist via MCP
        - Provide weekly reflections and mood trends analysis using 'analyze_weekly_trends'
        - Create follow-up reminders for important activities using 'create_reminder'
        - Show recent history with 'show_recent_history' to track progress
        - Reference past check-ins to show progress and patterns
        
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

    @function_tool
    async def create_todoist_tasks(
        self,
        ctx: RunContext[Userdata],
        tasks: Annotated[list[str], Field(description="List of task descriptions to create in Todoist")]
    ) -> str:
        """
        Create tasks in Todoist for the user's goals.
        Call this when user wants to turn their goals into actionable tasks.
        """
        api_token = os.getenv("TODOIST_API_TOKEN")
        if not api_token:
            return "Sorry, Todoist integration is not configured. Please set your TODOIST_API_TOKEN."
        
        api = TodoistAPI(api_token)
        created_tasks = []
        try:
            for task_desc in tasks:
                task = api.add_task(content=task_desc)
                created_tasks.append(f"'{task_desc}' (ID: {task.id})")
                logger.info(f"Created Todoist task: {task_desc} with ID {task.id}")
            
            return f"Successfully created {len(tasks)} tasks in Todoist: {', '.join(created_tasks)}. You can manage them in your Todoist app."
        except Exception as e:
            logger.error(f"Error creating Todoist tasks: {e}")
            return "Sorry, I couldn't create the tasks right now. Please check your Todoist API token and try again."

    @function_tool
    async def analyze_weekly_trends(
        self,
        ctx: RunContext[Userdata]
    ) -> str:
        """
        Analyze the last 7 days of wellness data to provide insights on mood and goal completion.
        """
        try:
            if not os.path.exists(JSON_FILE):
                return "No wellness history available yet. Let's start with today's check-in!"
            
            with open(JSON_FILE, "r") as f:
                history = json.load(f)
            
            # Get last 7 entries
            recent_entries = history[-7:] if len(history) >= 7 else history
            
            if not recent_entries:
                return "No recent data to analyze."
            
            # Analyze mood trends
            moods = [entry.get('mood', '').lower() for entry in recent_entries]
            positive_words = ['good', 'great', 'excellent', 'energetic', 'happy', 'positive']
            negative_words = ['tired', 'low', 'stressed', 'sad', 'anxious', 'bad']
            
            positive_count = sum(1 for mood in moods if any(word in mood for word in positive_words))
            negative_count = sum(1 for mood in moods if any(word in mood for word in negative_words))
            
            # Analyze goals
            total_goals = sum(len(entry.get('goals', [])) for entry in recent_entries)
            avg_goals = total_goals / len(recent_entries) if recent_entries else 0
            
            analysis = f"""
Over the last {len(recent_entries)} days:
- Mood trends: {positive_count} days with positive energy, {negative_count} days with lower energy
- Average goals per day: {avg_goals:.1f}
- Total goals set: {total_goals}

You're showing consistent commitment to your wellness journey! Keep up the great work.
"""
            return analysis.strip()
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return "I couldn't analyze your trends right now, but we can check again later."

    @function_tool
    async def create_reminder(
        self,
        ctx: RunContext[Userdata],
        activity: Annotated[str, Field(description="The activity to be reminded about")],
        time: Annotated[str, Field(description="When to do the activity (e.g., '6 pm', 'tomorrow morning')")]
    ) -> str:
        """
        Create a follow-up reminder for an important wellness activity in Todoist.
        Use this when user mentions specific timed activities they want to remember.
        """
        api_token = os.getenv("TODOIST_API_TOKEN")
        if not api_token:
            return "Sorry, Todoist integration is not configured. Please set your TODOIST_API_TOKEN."
        
        api = TodoistAPI(api_token)
        try:
            # Create a task with due date
            task_content = f"Reminder: {activity}"
            task = api.add_task(content=task_content, due_string=time)
            logger.info(f"Created Todoist reminder: {task_content} at {time} with ID {task.id}")
            
            return f"✅ Reminder created in Todoist! I'll help you remember to {activity} at {time}. Check your Todoist app for the task."
        except Exception as e:
            logger.error(f"Error creating reminder: {e}")
            return "Sorry, I couldn't create the reminder right now. Please check your Todoist API token and try again."

    @function_tool
    async def show_recent_history(
        self,
        ctx: RunContext[Userdata],
        days: Annotated[int, Field(description="Number of recent days to show (default 3)")] = 3
    ) -> str:
        """
        Show the user's recent wellness check-ins to help them see their progress.
        """
        try:
            if not os.path.exists(JSON_FILE):
                return "No wellness history available yet. Let's create your first check-in!"
            
            with open(JSON_FILE, "r") as f:
                history = json.load(f)
            
            recent_entries = history[-days:] if len(history) >= days else history
            
            if not recent_entries:
                return "No recent entries found."
            
            summary = "Here are your recent check-ins:\n\n"
            for i, entry in enumerate(reversed(recent_entries), 1):
                date = entry.get('timestamp', '')[:10]
                mood = entry.get('mood', 'Not specified')
                goals = ', '.join(entry.get('goals', []))
                summary += f"{i}. {date}: Mood - {mood}\n   Goals: {goals}\n\n"
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error showing history: {e}")
            return "I couldn't retrieve your history right now."


server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    # 1. Read JSON history before starting
    last_entry = get_last_checkin()
    history_summary = ""
    if last_entry:
        history_summary = f"Last check-in: {last_entry['timestamp'][:10]}, Mood: {last_entry['mood']}, Goals: {', '.join(last_entry['goals'])}"
    
    # Load full history for advanced analysis
    full_history = []
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                full_history = json.load(f)
        except:
            full_history = []
    
    userdata = Userdata(last_session_summary=history_summary)
    
    session = AgentSession[Userdata](
        userdata=userdata,
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash-lite"),
        tts=murf.TTS(voice="Alicia", model="Murf Falcon"),
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )

    await session.start(agent=WellnessAgent(userdata=userdata), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(server)