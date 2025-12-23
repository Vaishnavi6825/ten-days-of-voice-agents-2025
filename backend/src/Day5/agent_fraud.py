import logging
import json
import os
import asyncio
from datetime import datetime
from typing import Annotated, Optional
from dataclasses import dataclass
import random

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    RunContext,
    cli,
    function_tool,
    get_job_context,
)
from livekit.plugins import google, deepgram, silero, murf
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit import api
from pydantic import Field

from Day5.fraud_case import FraudCase
from Day5.fraud_database import (
    initialize_fraud_database,
    find_fraud_case_by_username,
    update_fraud_case,
    load_all_fraud_cases
)

load_dotenv()
logger = logging.getLogger("Fraud_Alert_Agent")

# --- JSON HELPER FUNCTIONS (Like Nykaa Agent) ---
FRAUD_CASES_FILE = "fraud_cases.json"

def save_fraud_case_to_json(case: FraudCase) -> dict:
    """
    Saves the fraud case to the JSON file.
    This mirrors the save_lead_to_json from Nykaa agent.
    """
    entry = {
        "case_id": case.case_id,
        "userName": case.userName,
        "securityIdentifier": case.securityIdentifier,
        "cardEnding": case.cardEnding,
        "transactionName": case.transactionName,
        "transactionAmount": case.transactionAmount,
        "transactionTime": case.transactionTime,
        "transactionCategory": case.transactionCategory,
        "transactionSource": case.transactionSource,
        "merchantLocation": case.merchantLocation,
        "securityQuestion": case.securityQuestion,
        "securityAnswer": case.securityAnswer,
        "status": case.status,
        "outcome_note": case.outcome_note,
        "timestamp": case.timestamp
    }
    
    # Load existing data or create new list
    if os.path.exists(FRAUD_CASES_FILE):
        with open(FRAUD_CASES_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []
    
    # Update the case if it exists, otherwise append
    case_index = -1
    for i, existing_case in enumerate(history):
        if existing_case.get("case_id") == case.case_id:
            case_index = i
            break
    
    if case_index >= 0:
        history[case_index] = entry
        logger.info(f"✅ Updated existing case {case.case_id} in JSON")
    else:
        history.append(entry)
        logger.info(f"✅ Added new case {case.case_id} to JSON")
    
    # Write back to file
    with open(FRAUD_CASES_FILE, "w") as f:
        json.dump(history, f, indent=4)
    
    logger.info(f"✅ Fraud case saved to {FRAUD_CASES_FILE}")
    return entry


@dataclass
class FraudContext:
    current_case: Optional[FraudCase] = None
    verification_passed: bool = False
    username_input: str = ""
    call_type: str = "inbound"  # inbound or outbound
    is_telephony: bool = False  # True if using actual phone call


async def hangup_call():
    """
    Terminate the current call for all participants.
    Used for both in-app and telephony calls.
    """
    ctx = cli.get_job_context()
    if ctx is None:
        logger.warning("⚠️ Not running in a job context, cannot hangup")
        return
    
    try:
        await ctx.api.room.delete_room(
            api.DeleteRoomRequest(
                room=ctx.room.name,
            )
        )
        logger.info(f"🔌 Hangup call - Room {ctx.room.name} deleted")
    except Exception as e:
        logger.error(f"❌ Error hanging up call: {str(e)}")


class FraudAlertAgent(Agent):
    def __init__(self, *, userdata: FraudContext) -> None:
        instructions = """
You are a professional Fraud Detection Representative for SecureBank, a trusted financial institution.

YOUR ROLE & RESPONSIBILITIES:
1. GREET & INTRODUCE:
   - Greet the customer warmly and professionally
   - Introduce yourself as SecureBank's Fraud Detection Team
   - Explain that you're calling about a suspicious transaction on their account
   - Keep tone calm, reassuring, and professional

2. VERIFICATION PROCESS:
   - Ask the customer for their username to find their case
   - Use the verify_customer tool to confirm identity using the security question
   - IF VERIFICATION PASSES: Proceed to transaction details
   - IF VERIFICATION FAILS: Politely apologize and end the call using end_call tool

3. READ TRANSACTION DETAILS:
   - Once verified, explain the suspicious transaction clearly
   - Include: merchant name, amount, card ending, time, location, category
   - Example: "We detected a transaction of ₹50,000 at Amazon Electronics on Nov 25 at 3:45 AM"

4. ASK FOR CONFIRMATION:
   - Ask: "Did you authorize this transaction?"
   - Listen carefully to their response (yes/no)
   - Be empathetic - they may be surprised

5. HANDLE OUTCOMES:
   - If YES (Customer confirms): Mark as SAFE
     * Thank them for confirming
     * Say the transaction is approved
   - If NO (Customer denies): Mark as FRAUDULENT
     * Take their concern seriously
     * Explain action: "We will immediately block your card and raise a dispute"
     * Assure them they won't be liable for unauthorized charges

6. END CALL:
   - Summarize what was done
   - Thank them for their time
   - Provide reassurance
   - Use the save_fraud_case tool to update the database
   - Use the end_call tool to terminate the session

IMPORTANT GUIDELINES:
- NEVER ask for full card numbers, PINs, passwords, or CVV
- Use ONLY the security question for verification (from database)
- Keep language professional, calm, and reassuring
- Be concise but thorough
- Show empathy and understanding
- ALWAYS use the save_fraud_case tool when the call ends to persist data
- Use end_call tool to properly terminate the conversation
"""

        super().__init__(
            instructions=instructions,
            tools=[
                # Tools are auto-detected via function_tool decorator
            ],
        )
        self.userdata = userdata

    @function_tool
    async def verify_customer(
        self,
        ctx: RunContext[FraudContext],
        username: Annotated[str, Field(description="Customer username to look up")],
        security_answer: Annotated[str, Field(description="Customer's answer to the security question")]
    ) -> str:
        """
        Verify customer identity using security question.
        Returns success or failure message.
        """
        case = find_fraud_case_by_username(username)
        
        if not case:
            logger.warning(f"❌ No case found for username '{username}'")
            return f"No case found for username '{username}'. Please try again."
        
        # Store case in context
        ctx.userdata.current_case = case
        ctx.userdata.username_input = username
        
        logger.info(f"📋 Security Question: {case.securityQuestion}")
        
        # Verify security answer (case-insensitive)
        if security_answer.lower().strip() == case.securityAnswer.lower().strip():
            ctx.userdata.verification_passed = True
            logger.info(f"✅ Verification PASSED for {username}")
            return f"Verification successful! I found a suspicious transaction on your account. Let me read the details."
        else:
            logger.warning(f"❌ Verification FAILED for {username} - Wrong security answer")
            return "I'm sorry, that answer doesn't match our records. For security reasons, I cannot proceed. Please contact our customer service line."

    @function_tool
    async def get_transaction_details(
        self,
        ctx: RunContext[FraudContext]
    ) -> str:
        """
        Retrieve and format the current fraud case transaction details.
        Use this to read details to the customer.
        """
        if not ctx.userdata.current_case:
            logger.error("❌ No active fraud case found")
            return "No transaction details available."
        
        case = ctx.userdata.current_case
        
        details = f"""
Here are the suspicious transaction details:

Merchant: {case.transactionName}
Amount: ₹{case.transactionAmount:,.2f}
Card Ending: {case.cardEnding}
Time: {case.transactionTime}
Location: {case.merchantLocation}
Category: {case.transactionCategory}
Source: {case.transactionSource}

Does this transaction look familiar to you?
"""
        logger.info(f"📊 Transaction Details:\n{details}")
        return details

    @function_tool
    async def save_fraud_case(
        self,
        ctx: RunContext[FraudContext],
        decision: Annotated[str, Field(description="'safe' or 'fraud' or 'failed'")],
        customer_response: Annotated[str, Field(description="Brief summary of customer's response")]
    ) -> str:
        """
        Save the fraud case decision to the JSON database.
        This mirrors save_lead_to_database from Nykaa agent.
        Call this BEFORE end_call tool.
        """
        if not ctx.userdata.current_case:
            logger.error("❌ No active fraud case found to save")
            return "Error: No active fraud case found."
        
        case = ctx.userdata.current_case
        
        # Map decision to status
        if decision.lower() == "safe":
            status = "confirmed_safe"
            note = f"Customer verified transaction as legitimate. {customer_response}"
        elif decision.lower() == "fraud":
            status = "confirmed_fraud"
            note = f"Customer denied transaction. Card blocked and dispute raised. {customer_response}"
        elif decision.lower() == "failed":
            status = "verification_failed"
            note = f"Customer verification failed. Call terminated. {customer_response}"
        else:
            status = "pending_review"
            note = customer_response
        
        # Update the case object
        case.status = status
        case.outcome_note = note
        case.timestamp = datetime.now().isoformat()
        
        # Save to JSON file
        try:
            saved_entry = save_fraud_case_to_json(case)
            logger.info(f"✅ Fraud case {case.case_id} saved with status: {status}")
            return f"✅ Case {case.case_id} updated successfully! Status: {status}. Data saved to fraud_cases.json"
        except Exception as e:
            logger.error(f"❌ Error saving fraud case to JSON: {str(e)}")
            return f"Error saving case: {str(e)}"

    @function_tool
    async def end_call(
        self,
        ctx: RunContext[FraudContext]
    ) -> str:
        """
        Terminate the call gracefully for both in-app and telephony calls.
        Always call save_fraud_case BEFORE this tool.
        """
        try:
            # Add a small delay to let the agent finish speaking
            await asyncio.sleep(1)
            
            call_type = "telephony (real phone)" if ctx.userdata.is_telephony else "in-app"
            logger.info(f"🔌 Ending {call_type} call...")
            
            # Hangup the call
            await hangup_call()
            
            logger.info(f"✅ Call ended successfully")
            return "Call terminated. Thank you for using SecureBank Fraud Detection."
        except Exception as e:
            logger.error(f"❌ Error ending call: {str(e)}")
            return f"Error ending call: {str(e)}"


async def hangup_call():
    ctx = get_job_context()
    if ctx is None:
        return
    await ctx.api.room.delete_room(api.DeleteRoomRequest(room=ctx.room.name))


server = AgentServer()


@server.rtc_session(agent_name="fraud-alert-agent")
async def main(ctx: JobContext) -> None:
    """
    Main entry point for the Fraud Alert Agent.
    Handles both in-app calls and telephony calls.
    Agent dispatch ensures explicit routing for telephony.
    """
    logger.info("=" * 60)
    logger.info("🚀 FRAUD ALERT VOICE AGENT INITIALIZED")
    logger.info("=" * 60)
    
    # Initialize fraud database
    logger.info("🔄 Initializing fraud database...")
    initialize_fraud_database()
    
    # Verify fraud_cases.json exists
    if os.path.exists(FRAUD_CASES_FILE):
        with open(FRAUD_CASES_FILE, "r") as f:
            cases = json.load(f)
            logger.info(f"✅ Fraud database initialized with {len(cases)} cases")
            for case in cases:
                logger.info(f"   - {case['case_id']}: {case['userName']} ({case['status']})")
    else:
        logger.error("❌ fraud_cases.json not found!")
    
    # Detect call type
    dial_info = json.loads(ctx.job.metadata or '{}')
    phone_number = dial_info.get("phone_number")
    is_outbound = phone_number is not None
    is_telephony = is_outbound  # Outbound calls are telephony; inbound detected separately
    
    # Create fraud context
    userdata = FraudContext(is_telephony=is_telephony)
    
    logger.info(f"📞 Call Type: {'TELEPHONY (Outbound)' if is_outbound else 'IN-APP or Inbound Call'}")
    logger.info(f"🏠 Room: {ctx.room.name}")
    
    # For outbound calls, initiate the SIP call
    if phone_number:
        sip_trunk_id = 'ST_xxxx'  # Replace with your actual outbound trunk ID from `lk sip outbound list`
        try:
            await ctx.api.sip.create_sip_participant(api.CreateSIPParticipantRequest(
                room_name=ctx.room.name,
                sip_trunk_id=sip_trunk_id,
                sip_call_to=phone_number,
                participant_identity=phone_number,
                wait_until_answered=True,
            ))
            logger.info("📞 Outbound call initiated successfully")
        except api.TwirpError as e:
            logger.error(f"❌ Error creating SIP participant: {e.message}, SIP status: {e.metadata.get('sip_status_code')} {e.metadata.get('sip_status')}")
            ctx.shutdown()
            return
    
    # Create and start agent session
    logger.info("🔧 Configuring LiveKit Agent Session...")
    session = AgentSession[FraudContext](
        userdata=userdata,
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-pro"),
        tts=google.TTS(),
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
    )

    await session.start(agent=FraudAlertAgent(userdata=userdata), room=ctx.room)
    
    # For inbound calls, greet the user
    if not is_outbound:
        await session.generate_reply(instructions="Greet the user and offer your assistance.")
    
    logger.info("=" * 60)
    logger.info("✅ AGENT SESSION COMPLETED")
    logger.info("=" * 60)


if __name__ == "__main__":
    cli.run_app(server)