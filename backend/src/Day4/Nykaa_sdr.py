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

from Day4.nykaa_database import FAQ_DATA, find_faq_answer
from Day4.nykaa_order import LeadData

load_dotenv()
logger = logging.getLogger("Nykaa_sdr")

# --- JSON HELPER FUNCTIONS ---
LEADS_FILE = "nykaa_leads.json"

def get_last_lead():
    """Reads the JSON file and returns the last lead if it exists."""
    if not os.path.exists(LEADS_FILE):
        return None
    
    try:
        with open(LEADS_FILE, "r") as f:
            data = json.load(f)
            if data:
                return data[-1]
    except Exception:
        return None
    return None

def save_lead_to_json(lead_data: LeadData) -> dict:
    """Saves the current lead to the JSON file."""
    entry = {
        "lead_id": lead_data.lead_id,
        "timestamp": datetime.now().isoformat(),
        "name": lead_data.name,
        "email": lead_data.email,
        "company": lead_data.company,
        "role": lead_data.role,
        "use_case": lead_data.use_case,
        "team_size": lead_data.team_size,
        "timeline": lead_data.timeline,
        "call_summary": lead_data.call_summary
    }
    
    # Load existing data or create new list
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []
        
    history.append(entry)
    
    # Write back to file
    with open(LEADS_FILE, "w") as f:
        json.dump(history, f, indent=4)
    
    return entry

@dataclass
class UserContext:
    company_context: str
    faq_context: str

class NykaaSDRAgent(Agent):
    def __init__(self, *, userdata: UserContext) -> None:
        # Build dynamic context
        context_str = f"""
{userdata.company_context}

FAQ Knowledge Base:
{userdata.faq_context}
"""

        instructions = f"""
You are a professional Sales Development Representative (SDR) for Nykaa, India's leading online beauty and wellness platform.

COMPANY CONTEXT:
{context_str}

YOUR ROLE:
1. Greet visitors warmly and introduce yourself as a Nykaa SDR
2. Ask what brought them here and what they're working on
3. Answer product/company/pricing questions using the FAQ knowledge base provided
4. Understand their specific needs and use case
5. Naturally collect key lead information during the conversation:
   - Name, Email, Company
   - Job Role
   - Use Case (what they want to use Nykaa for)
   - Team Size
   - Timeline (now/soon/later)
6. When the conversation is wrapping up (user says "that's all", "I'm done", "thanks", etc.):
   - Provide a brief verbal summary of who they are and what they need
   - Use the save_lead_to_database tool to save the lead
   - Confirm the save and wish them well

IMPORTANT GUIDELINES:
- Be warm, professional, and genuinely interested in their needs
- Only answer questions using the FAQ data provided - don't make up details
- If asked something not in the FAQ, say "That's a great question! Let me note that down for our team"
- Keep track of what you learn about them naturally - don't make it feel like a rigid form
- When saving the lead, summarize their key needs and interests in 1-2 sentences
"""

        super().__init__(
            instructions=instructions,
            tools=[
                # Tools are auto-detected
            ],
        )

    @function_tool
    async def save_lead_to_database(
        self,
        ctx: RunContext[UserContext],
        name: Annotated[str, Field(description="Full name of the prospect")],
        email: Annotated[str, Field(description="Email address of the prospect")],
        company: Annotated[Optional[str], Field(description="Company name (can be 'Self-Employed' or 'Not Specified')")],
        role: Annotated[Optional[str], Field(description="Job role or position")],
        use_case: Annotated[str, Field(description="What they want to use Nykaa for (e.g., 'personal beauty shopping', 'professional beautician looking for wholesale')")],
        team_size: Annotated[Optional[str], Field(description="Team size if applicable (e.g., '1', '5-10', '10-50')")],
        timeline: Annotated[str, Field(description="Timeline: 'now', 'soon' (next 2-3 weeks), or 'later'")],
        call_summary: Annotated[str, Field(description="1-2 sentence summary of their key needs and interests")]
    ) -> str:
        """
        Save the lead information to the JSON database at the END of the conversation.
        Call this tool when the user indicates they're done (says goodbye, thanks, etc).
        """
        lead_data = LeadData(
            name=name,
            email=email,
            company=company or "Not Specified",
            role=role or "Not Specified",
            use_case=use_case,
            team_size=team_size or "Not Specified",
            timeline=timeline,
            call_summary=call_summary
        )
        save_lead_to_json(lead_data)
        return f"Lead saved successfully! {name} from {lead_data.company} has been added to our pipeline."


server = AgentServer()

@server.rtc_session
async def main(ctx: JobContext) -> None:
    # Build context for the agent
    company_context = """
ABOUT NYKAA:
Nykaa is India's leading omnichannel beauty, wellness, and fashion platform.
- Founded in 2012 by Falguni Nayar
- First Indian unicorn startup headed by a woman
- Listed on NSE and BSE (November 2021)
- 100+ physical stores + online presence
- Over 1 lakh beauty products from 2400+ brands
- Headquarters: Mumbai

WHAT WE OFFER:
✓ Makeup & Cosmetics (lipsticks, foundations, eyeshadow, mascaras, etc)
✓ Skincare (creams, masks, serums, cleansers)
✓ Haircare & Styling
✓ Fragrances & Perfumes
✓ Bath & Body Products
✓ Wellness Products
✓ Fashion & Accessories
✓ Beauty Appliances
✓ Men's Grooming (Nykaa Man)
✓ Luxury Brands (MAC, Dior, HUDA Beauty, Charlotte Tilbury)

NYKAA PRO (Professional Program):
- Exclusive membership for salons, makeup artists, beauticians, hair stylists, academies
- 100+ professional-relevant brands
- Exclusive offers and GST benefits
- 100% genuine products sourced directly from brands
- Masterclasses and educational content
"""

    faq_context = """
NYKAA FAQ & KEY INFORMATION:

Q: What does Nykaa do?
A: Nykaa is an omnichannel beauty, wellness, and fashion retailer. We offer makeup, skincare, haircare, fragrances, wellness products, and fashion items from 2400+ brands. Shop online at Nykaa.com or visit one of our 100+ stores.

Q: Is there a free tier or trial?
A: For personal shoppers, you can browse and shop on Nykaa.com without membership. For professionals, we offer Nykaa PRO membership - apply at nykaa.com/pro-intro with business proof.

Q: Who is Nykaa for?
A: Everyone! Personal beauty shoppers (men, women), professionals (makeup artists, beauticians, hair stylists, salon owners), fashion enthusiasts, and wellness seekers.

Q: What brands are available?
A: We carry 2400+ brands including luxury (MAC, Dior, HUDA Beauty), popular Indian brands (Lakme, Nykaa Cosmetics, Naturals), and international brands (L'Oreal, Charlotte Tilbury, Maybelline).

Q: What is Nykaa PRO?
A: Professional membership program for beauty professionals offering exclusive deals on 100+ professional brands, GST benefits, masterclasses, and priority support.

Q: How do I become a Nykaa PRO member?
A: Visit nykaa.com/pro-intro, sign up with your professional proof (business card, salon license, etc), and we verify within 72 hours.

Q: What are delivery times?
A: Typically 3 days delivery. Free shipping on most orders. Cash on delivery available.

Q: Do you have physical stores?
A: Yes! 100+ Nykaa stores across India. Store formats include Nykaa Luxe (luxury brands), Nykaa On Trend (popular items), and Beauty Kiosks.

Q: What about returns and exchanges?
A: We accept returns/exchanges within our policy. Details available on Nykaa.com or call customer service.

Q: Is everything on Nykaa authentic?
A: Yes! 100% genuine products sourced directly from brands. We have strict quality checks and authentication processes.

Q: Do you have men's products?
A: Yes! Nykaa Man specializes in men's grooming - shaving creams, beard trimmers, hair care, and wellness products.

Q: What about wellness products?
A: We have a full wellness range including supplements, skincare focused on wellness, bath products, and health-focused items.
"""

    userdata = UserContext(
        company_context=company_context,
        faq_context=faq_context
    )
    
    session = AgentSession[UserContext](
        userdata=userdata,
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-pro"),
        tts=murf.TTS(model="en-US-falcon"),
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )

    await session.start(agent=NykaaSDRAgent(userdata=userdata), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(server)