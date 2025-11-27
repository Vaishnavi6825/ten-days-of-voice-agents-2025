# Day 6: Fraud Alert Voice Agent 🚨

## Project Overview
For Day 6, I built a specialized **Fraud Detection Voice Agent** for a fictional bank ("SecureBank"). The goal was to create a secure, voice-first interface for verifying suspicious transactions without requiring a human agent.

This agent acts as a proactive security guard. It calls the user, verifies their identity using a security question, reads out transaction details, and updates the fraud case status in real-time based on the user's response.

## Key Features
- **Persona:** "Alex", a calm and professional Fraud Detection Specialist.
- **Secure Verification:** Dynamic security questions (e.g., "First pet's name") to authenticate the user before discussing sensitive data.
- **Database Integration:** Reads transaction details from a mock database and writes the final status (`safe` vs `fraud`) back to disk.

## File Structure
- `src/fraud_case.py`: Defines the data structure for a fraud case (User, Transaction Amount, Merchant, Status).
- `src/fraud_database.py`: Manages the mock database (JSON file), handling data retrieval and status updates.
- `src/agent_fraud.py`: The main agent logic. It manages the conversation flow, tool calling for verification, and voice interaction.

## Tech Stack
* **Orchestration:** LiveKit Agents
* **LLM:** Google Gemini 1.5 Flash
* **STT/TTS:** Deepgram Nova-3
* **Language:** Python 3.10+

3.  **Test Scenarios:**
    * **John:** Safe user (Security Answer: "max").
    * **Sarah:** Fraud victim (Security Answer: "london").

Linkedin:[https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7399738557604745216-PVVt?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD6tG3MBYWx9mOEBXuTEYqfqcrMbrpxUBwE]

---
