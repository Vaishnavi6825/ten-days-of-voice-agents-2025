# order.py
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid

class WellnessItem(BaseModel):
    """Base class for logged items."""
    log_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class WellnessLog(WellnessItem):
    """A health activity log."""
    activity_id: str
    quantity: int = 0  # Amount (e.g., 30 mins, 500ml)
    unit: str = ""     # Unit name
    notes: Optional[str] = None

class WellnessState:
    """Manages the daily health logs."""
    
    def __init__(self, items: dict = None):
        self.items: dict[str, WellnessLog] = items or {}
    
    async def add(self, item: WellnessLog) -> None:
        """Add an activity to the daily log."""
        self.items[item.log_id] = item
    
    async def remove(self, log_id: str) -> WellnessLog:
        if log_id not in self.items:
            raise ValueError(f"Log with ID {log_id} not found")
        return self.items.pop(log_id)
    
    def clear(self) -> None:
        self.items.clear()