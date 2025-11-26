# nykaa_order.py
from typing import Optional
from pydantic import BaseModel, Field
import uuid

class LeadItem(BaseModel):
    """Base class for lead items."""
    lead_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class LeadData(LeadItem):
    """Sales lead information from SDR conversation."""
    name: str
    email: str
    company: str = "Not Specified"
    role: str = "Not Specified"
    use_case: str  # What they want to use Nykaa for
    team_size: str = "Not Specified"  # 1, 5-10, 10-50, 50+, etc
    timeline: str  # "now", "soon", "later"
    call_summary: str  # 1-2 sentence summary

class LeadState:
    """Manages leads collected during the session."""
    
    def __init__(self, leads: dict = None):
        self.leads: dict[str, LeadData] = leads or {}
    
    async def add_lead(self, lead: LeadData) -> None:
        """Add a new lead."""
        self.leads[lead.lead_id] = lead
    
    async def get_lead(self, lead_id: str) -> Optional[LeadData]:
        """Retrieve a lead by ID."""
        return self.leads.get(lead_id)
    
    async def remove_lead(self, lead_id: str) -> LeadData:
        """Remove a lead."""
        if lead_id not in self.leads:
            raise ValueError(f"Lead with ID {lead_id} not found")
        return self.leads.pop(lead_id)
    
    def get_all_leads(self) -> list[LeadData]:
        """Get all collected leads."""
        return list(self.leads.values())
    
    def clear(self) -> None:
        """Clear all leads."""
        self.leads.clear()


# --- LEAD SCORING & QUALIFICATION ---
class LeadQualification:
    """Helper class to score and qualify leads."""
    
    # Timeline scores
    TIMELINE_SCORES = {
        "now": 10,
        "soon": 7,
        "later": 3
    }
    
    # Use case priority (higher = more valuable)
    USE_CASE_PRIORITY = {
        "professional_wholesale": 10,  # Salon, beautician, makeup artist
        "business_reseller": 8,  # Small business
        "personal_shopping": 5,  # Individual consumer
        "other": 3
    }
    
    @staticmethod
    def categorize_use_case(use_case: str) -> str:
        """Categorize the use case."""
        use_case_lower = use_case.lower()
        
        if any(word in use_case_lower for word in ["salon", "beautician", "makeup artist", "professional", "wholesale"]):
            return "professional_wholesale"
        elif any(word in use_case_lower for word in ["resell", "business", "store"]):
            return "business_reseller"
        elif any(word in use_case_lower for word in ["personal", "myself", "shopping", "own use"]):
            return "personal_shopping"
        else:
            return "other"
    
    @staticmethod
    def score_lead(lead: LeadData) -> int:
        """
        Score a lead based on timeline, use case, and other factors.
        Returns a score out of 100.
        """
        score = 0
        
        # Timeline scoring
        timeline_lower = lead.timeline.lower()
        score += LeadQualification.TIMELINE_SCORES.get(timeline_lower, 5)
        
        # Use case scoring
        use_case_category = LeadQualification.categorize_use_case(lead.use_case)
        score += LeadQualification.USE_CASE_PRIORITY.get(use_case_category, 3)
        
        # Team size bonus (professionals typically have larger teams)
        if lead.team_size != "Not Specified" and lead.team_size != "1":
            score += 5
        
        # Company bonus (B2B > personal)
        if lead.company != "Not Specified" and lead.company.lower() not in ["self-employed", "freelance"]:
            score += 5
        
        return min(score, 100)  # Cap at 100