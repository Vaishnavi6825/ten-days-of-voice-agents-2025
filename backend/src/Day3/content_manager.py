import json
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Lesson:
    id: str
    title: str
    summary: str
    sample_question: str

class ContentManager:
    def __init__(self):
        self.lessons = {}
        
        # This magic line finds the JSON file in the SAME folder as this script
        # No matter where you run the command from, this will work.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "tutor_content.json")
        
        try:
            with open(path, "r") as f:
                data = json.load(f)
                for item in data:
                    self.lessons[item['id']] = Lesson(**item)
            print(f"SUCCESS: Loaded {len(self.lessons)} lessons from {path}")
        except Exception as e:
            print(f"ERROR: Could not load content from {path}")
            print(f"Details: {e}")

    def get_lesson(self, topic_id: str) -> Optional[Lesson]:
        return self.lessons.get(topic_id)

    def get_all_topics(self) -> str:
        return ", ".join([l.title for l in self.lessons.values()])