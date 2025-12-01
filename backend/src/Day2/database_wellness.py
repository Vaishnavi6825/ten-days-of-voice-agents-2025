# database.py
from dataclasses import dataclass
from typing import List, Optional

# --- Configuration ---
COMMON_INSTRUCTIONS = """
You are a supportive and motivating Health & Wellness Voice Companion.
Your job is to help users track their health activities, water intake, and mindfulness sessions.
Always be encouraging. When a user logs an activity, ask how they feel or give them a compliment.
If the user is unsure what to do, suggest a quick breathing exercise or a stretch.
"""

@dataclass
class MenuItem:
    id: str
    name: str
    category: str  # exercise, nutrition, mindfulness
    unit: str = "" # e.g., "mins", "steps", "liters"

# --- Data ---
raw_data = [
    # Exercise
    MenuItem("running", "Running", "exercise", "mins"),
    MenuItem("yoga", "Yoga Session", "exercise", "mins"),
    MenuItem("walking", "Walking", "exercise", "steps"),
    MenuItem("pushups", "Push-ups", "exercise", "reps"),
    MenuItem("cycling", "Cycling", "exercise", "km"),
    
    # Nutrition/Hydration
    MenuItem("water", "Water", "nutrition", "ml"),
    MenuItem("meal", "Healthy Meal", "nutrition", "calories"),
    MenuItem("fruits", "Eating Fruits", "nutrition", "portions"),

    # Mindfulness/Mental Health
    MenuItem("meditation", "Meditation", "mindfulness", "mins"),
    MenuItem("breathing", "Breathing Exercise", "mindfulness", "mins"),
    MenuItem("journaling", "Journaling", "mindfulness", "mins"),
]

class FakeDB:
    async def list_exercises(self) -> List[MenuItem]:
        return [i for i in raw_data if i.category == "exercise"]

    async def list_nutrition(self) -> List[MenuItem]:
        return [i for i in raw_data if i.category == "nutrition"]
    
    async def list_mindfulness(self) -> List[MenuItem]:
        return [i for i in raw_data if i.category == "mindfulness"]

# Helper to find items
def find_items_by_id(items: List[MenuItem], item_id: str) -> Optional[MenuItem]:
    for item in items:
        if item.id == item_id:
            return item
    return None

def menu_instructions(category: str, items: List[MenuItem]) -> str:
    item_names = ", ".join([f"{i.name} ({i.id})" for i in items])
    return f"Available {category}: {item_names}"